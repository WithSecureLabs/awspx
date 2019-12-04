import neo4j from 'neo4j-driver'

export default {

    install: function (Vue, ) {

        var auth = neo4j.auth.basic("neo4j", "neo4j");
        var driver = neo4j.driver(
            "bolt://localhost",
            auth, {
                encrypted: false
            });
        var session = driver.session()

        Object.defineProperty(
            Vue.prototype,
            '$neo4j', {
                value: session
            }
        );

    },

    methods: {
        
    },
}
