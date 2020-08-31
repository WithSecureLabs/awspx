import neo4j from 'neo4j-driver'


export default {

    methods: {

        /* Generic interface for formatting Neo4j result set. */

        run(statement, driver, selectors = ["Graph", "Text"]) {

            const Graph = {};
            const Text = [];

            function node(element) {

                const properties = cast(element.properties);

                if (selectors.includes("Graph")) {

                    let id = "n" + element.identity.toString();
                    if (id in Graph) return properties;

                    const node = {};
                    const names = Object.keys(element.properties)
                        .filter(k => (/name/i).test(k))
                        .sort((a, b) => a.length - b.length)

                    node.group = "nodes";
                    node.classes = element.labels.sort();
                    node.scratch = {};
                    node.data = {
                        id: id,
                        properties: properties,
                        name: (names.length > 0) ?
                            element.properties[names[0]] :
                            node.classes[0],
                    };

                    Graph[id] = node
                }
                return properties;
            }

            function edge(element) {
                return cast(element.properties);
            }

            function path(element) {

                const properties = cast([
                    element.start.properties,
                    element.relationship.properties,
                    element.end.properties
                ])

                if (selectors.includes("Graph")) {

                    const id = "e" + element.relationship.identity.toString();

                    if (id in Graph)
                        return properties

                    const path = {};
                    const source = "n" + element.relationship.start.toString();
                    const target = "n" + element.relationship.end.toString();
                    const names = Object.keys(properties[1])
                        .filter(k => (/name/i).test(k))
                        .sort((a, b) => a.length - b.length)

                    node(element.start);
                    node(element.end);

                    path.group = "edges";
                    path.classes = [element.relationship.type];
                    path.scratch = {}
                    path.data = {
                        id: id,
                        source: source,
                        target: target,
                        properties: properties[1],
                        name: (names.length > 0) ?
                            properties[1][names[0]] :
                            path.classes[0],
                    };

                    Graph[id] = path;
                }

                return properties
            }

            function cast(result) {

                // Node
                if (result !== null &&
                    typeof result == "object" &&
                    ["identity", "labels", "properties"].every(
                        k => Object.keys(result).includes(k))
                )
                    return JSON.stringify(node(result), null, 2)

                // Edge
                else if (
                    result !== null &&
                    typeof result === "object" &&
                    ["identity", "start", "end", "type", "properties"].every(
                        k => Object.keys(result).includes(k))
                )
                    return JSON.stringify(edge(result), null, 2)
                // Path
                else if (
                    result !== null &&
                    typeof result === "object" &&
                    Object.keys(result).includes("segments") &&
                    result.segments.length > 0
                )
                    return JSON.stringify(result.segments.map(segment => {
                        return path(segment)
                    }), null, 2);

                else if (!selectors.includes("Text"))
                    return null
                // Number
                else if (result === null ||
                    typeof result === "number")
                    return result;
                // Boolean
                else if (
                    typeof result === "boolean" ||
                    result.toString().toLowerCase() == "true" ||
                    result.toString().toLowerCase() == "false"
                )
                    return result.toString().toLowerCase() === "true";
                // Integer
                else if (
                    typeof result === "object" &&
                    Object.keys(result).includes("high") &&
                    Object.keys(result).includes("low")
                )
                    return parseInt(result.toString());
                // String
                if (typeof result === "string") return result.toString();
                // Array
                else if (Array.isArray(result)) return result.map(e => cast(e));
                else if (typeof result === "object") {
                    Object.keys(result).map(k => (result[k] = cast(result[k])));
                    return result;
                }
                // Unknown
                //else console.log(result, "is of an unknown type");
                return null;
            }

            if (!Array.isArray(selectors))
                selectors = ["Graph", "Text"]

            const neo4j = driver.session();
            return neo4j
                .run(statement)
                .then(response => {
                    response.records.forEach(function (record) {
                        let result = {};
                        for (var i = 0; i < record._fields.length; i++) {
                            result[record.keys[i]] = cast(record._fields[i]);
                        }
                        if (selectors.includes("Text"))
                            Text.push(result);
                    });

                    return Promise.resolve({
                        Text: Text,
                        Graph: Object.keys(Graph).length != 0
                            ? Object.keys(Graph).map(k => Graph[k])
                            : []
                    });
                })
        },

        /* Awspx specific stylization (schema abstraction and element styling) */

        stylize(results) {

            const Graph = [
                ...(Array.isArray(results.Graph))
                    ? results.Graph
                    : []
            ]

            const nodes = []
            const edges = []

            for (let i = 0; i < Graph.length; i++) {

                let element = Graph[i];

                element.data.type = element.classes
                    .filter(c => c.includes("::"))
                    .concat(element.classes)[0]

                element.classes = element.classes
                    .map(e => e.split("::")).flat()

                if (element.group === "nodes"
                    && ["Resource", "Generic", "External", "Admin", "CatchAll"]
                        .filter(c => element.classes.indexOf(c) != -1).length > 0
                ) nodes.push(element)

                else if (element.group === "edges"
                    && ["TRANSITIVE", "ASSOCIATIVE"]
                        .filter(c => element.classes.indexOf(c) != -1).length > 0
                ) edges.push(element)

                else if (element.group === "edges"
                    && ["ATTACK", "TRUSTS"]
                        .filter(c => element.classes.indexOf(c) != -1).length > 0
                ) { /* pass */ }

                else if (element.classes.includes("ACTION")) {
                    element.classes.push(element.data.properties.Access)
                    element.classes.push(element.data.properties.Effect)
                    if (Object.keys(element.data.properties).includes("Condition")) {
                        if (element.data.properties.Condition === "[]")
                            delete element.data.properties.Condition
                        else
                            element.classes.push("Conditional")
                    }
                    edges.push(element)
                }

                else if (element.classes.includes("Pattern")) {

                    const source = Graph.find(e => e.classes.includes("ATTACK")
                        && e.data.target === element.data.id)

                    if (typeof source === 'undefined')
                        continue

                    edges.push.apply(edges, Graph.filter(e => (e.group === "edges"
                        && e.data.source === element.data.id)).map(e => {
                            return {
                                ...e,
                                data: {
                                    ...e.data,
                                    source: source.data.source
                                }
                            }
                        }));
                }
                else { /* unhandled */ }
            }

            return Promise.resolve({
                ...results,
                Graph: nodes.concat(edges)
            });


        },

        /* Collapse action elements into a collection of actions */
        bundle_actions(results, with_size_greater_than = 1) {

            let collections = {}
            let Graph = results.Graph.filter(e => {
                if (e.classes.includes("ACTION")) {
                    const id = `a${e.data.source}-${e.data.target}`
                    const access = e.data.properties.Access
                    if (!(id in collections)) collections[id] = {}
                    if (!(access in collections[id])) collections[id][access] = []
                    collections[id][access].push(e)
                    return false
                }
                return true;
            });

            Object.keys(collections).forEach(k => {

                const actions = Object.keys(collections[k])
                    .map(a => collections[k][a]).flat()

                if (actions.length <= with_size_greater_than)
                    Graph.push.apply(Graph, actions)

                else Graph.push({
                    classes: ["ACTIONS"].concat(Array.from(new Set(actions.map(a => a.data.properties.Effect)))),
                    data: {
                        id: k,
                        name: (actions.length > 1) ? `${actions.length} Actions` : `1 Action`,
                        source: actions[0].data.source,
                        target: actions[0].data.target,
                        properties: collections[k]
                    }
                })
            })

            return Promise.resolve({
                ...results,
                Graph: Graph
            });
        },

        // TODO:
        collapse_branches(results) {
            return Promise.resolve(results)
        }
    },
    install: function (Vue,) {

        const driver = Vue.observable({ value: {} });
        const error = Vue.observable({ value: {} });
        const state = Vue.observable({ statement: "", active: false });

        const auth = Vue.observable({
            uri: `bolt://${new URL(location.href).host}:7687`,
            username: "neo4j",
            password: "password"
        });

        Object.defineProperty(Vue.prototype, 'neo4j', {
            value: {
                auth: auth,
                state: state,
                error: error
            }
        });

        Object.defineProperty(Vue.prototype.neo4j, 'error', {
            get() { return error.value },
            set(value) { error.value = value }
        });

        Vue.prototype.neo4j.setup = (
            uri = auth.uri,
            username = auth.username,
            password = auth.password
        ) => {

            auth.uri = uri;
            auth.username = username;
            auth.password = password;

            driver.value = neo4j.driver(
                uri, neo4j.auth.basic(username, password), {
                encrypted: false
            })
        }

        Vue.prototype.neo4j.test = (
            uri = auth.uri,
            username = auth.username,
            password = auth.password
        ) => {
            try {
                const connection = neo4j.driver(
                    uri, neo4j.auth.basic(username, password), {
                    encrypted: false
                })
                return this.methods.run("RETURN 1", connection).then(
                ).catch(e => {
                    return new Promise(() => {
                        throw e
                    })
                })
            } catch (e) {
                return new Promise(() => {
                    throw e
                })
            }
        }

        Vue.prototype.neo4j.run = (
            statement,
            suppress_error = true,
            connection = driver.value,
            selectors = ["Graph", "Text"]
        ) => {

            if (connection.constructor.name !== "Driver") {
                return Promise.resolve({
                    Text: [],
                    Graph: []
                })
            }

            const leniency = setTimeout(function () { state.active = true; }, 200);
            state.statement = statement;
            error.value = {};

            return this.methods.run(statement, connection, selectors)
                // Comment out the following 3 '.then' lines to genericize this component.
                .then(r => this.methods.stylize(r))
                .then(r => this.methods.bundle_actions(r))
                .then(r => this.methods.collapse_branches(r))
                .catch(e => {
                    error.value = e;
                    if (suppress_error) {
                        return Promise.resolve({
                            Text: [],
                            Graph: []
                        })
                    } else throw e
                })
                .finally(() => {
                    clearTimeout(leniency);
                    state.active = false;
                });
        }
    },
}
