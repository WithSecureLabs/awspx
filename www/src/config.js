import icons from './icons.js'
import colors from 'vuetify/lib/util/colors'

export const access = {

    "Allow": colors.green.base,
    "Deny": colors.red.base,
    "List": colors.yellow.base,
    "Read": colors.pink.darken1,
    "Write": colors.indigo.darken2,
    "Tagging": colors.teal.darken1,
    "Permissions Management": colors.deepPurple.darken1,
}

const cache = {}
const badge = (n, m) => {

    if (!(Object.keys(cache).includes(m)))
        cache[m] = {}

    if (!(n.data().type in cache[m])) {

        let svg = decodeURIComponent(n.style("background-image")).split('<svg ')
        let vb = svg[1].match(/viewBox="([-\.\d]+) ([-\.\d]+) ([-\.\d]+) ([-\.\d]+)"/i)

        if (vb === null || vb.length < 4)
            return n.style("background-image")

        vb = vb.splice(1, 4).map(i => parseFloat(i))

        const width = 2 * vb[2] * 0.0125
        const length = 9 * vb[3] * 0.0125

        const radius = 0.5 * length + 1.5 * width
        const dx = vb[0] + vb[2] - 2 * radius;
        const dy = vb[1] + radius;

        const suffix = `<g fill="#FFF">` +
            `<circle fill="${(m === "collapsible") ? "#6cae3e" : "black"}"` +
            `   cx="${dx + Math.max(length, width) / 2}" ` +
            `   cy="${dy + Math.max(length, width) / 2}" r="${radius}"/>` +
            `<rect x="${dx}" y="${dy + Math.abs(length - width) / 2}" width="${length}" height="${width}"/>` +
            ((m === "collapsible") ?
                `<rect x="${dx + Math.abs(length - width) / 2}" y="${dy}" width="${width}" height="${length}"/>` :
                ""
            ) + `</g>`

        cache[m][n.data().type] = 'data:image/svg+xml;utf8,' + encodeURIComponent(
            '<svg ' +
            svg[1].replace("</svg>", suffix + "</svg>"));
    }

    return cache[m][n.data().type]
}

export default {

    graph: {

        style: [{
            selector: 'node',
            style: {
                'font-family': 'Roboto Mono, monospace',
                'font-size': '12px',
                'height': 75,
                'width': 75,
                'label': 'data (name)',

                'background-color': 'white',
                'border-color': 'black',
                'border-width': 0.2,

                'text-halign': 'center',
                'text-valign': 'bottom',
                'color': 'White',
                'text-background-color': 'Black',
                'text-background-shape': 'roundrectangle',
                'text-background-padding': '2px',
                'text-background-opacity': '1',
                'text-wrap': 'ellipsis',
                'text-max-width': '160px',
            }
        },

        {
            selector: 'edge',
            style: {

                'font-family': 'Roboto Mono, monospace',
                'font-size': '6px',

                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'width': '1px',
                'line-color': "#999999",
                'color': 'White',
                'text-rotation': 'autorotate',
                'text-background-color': 'Black',
                'text-background-shape': 'roundrectangle',
                'text-background-padding': '6px',
                'text-background-opacity': '1',
                'text-wrap': 'ellipsis',
                'text-max-width': '50px',
                'z-index': '3',
            }
        },
        {
            selector: 'node.AWS',
            style: {
                'background-image': function (n) {
                    return n.data().type.split('::').reduce((o, k) => {
                        return Object.keys(o).includes(k) ? o[k] : icons.AWS.Resource
                    }, icons)
                },
            }
        },
        {
            selector: 'node.Admin',
            style: {
                'background-image': icons.Admin,
            }
        },
        {
            selector: 'node.CatchAll',
            style: {
                'background-image': icons.CatchAll,
            }
        },
        {
            selector: 'node.Internet.Domain',
            style: {
                'background-image': icons.Internet.Domain,
            }
        },
        {
            selector: 'edge.TRANSITIVE',
            style: {
                'width': '2',
            }
        },
        {
            selector: 'edge.ASSOCIATIVE',
            style: {
                'target-arrow-shape': 'none',
                'line-style': 'dotted'
            }
        },
        {
            selector: 'edge.ATTACK',
            style: {
                'line-style': 'dashed',
                'line-color': 'Maroon'
            }
        },
        {
            selector: 'edge.TRUSTS',
            style: {
                'width': '1px',
                'label': 'Trusts',
                'color': 'Black',
                'font-size': '10px',
                'line-color': 'Gold',
                'text-rotation': 'autorotate',
                'text-background-color': 'White',
                'text-background-opacity': '1',
                'text-max-width': '1000px',
            }
        },
        {
            selector: 'edge.ACTION',
            style: {
                "line-fill": "linear-gradient",
                'target-arrow-color': (e) => `${access[e.data("properties").Access]}`,
                'line-gradient-stop-colors': (e) => `${access[e.data("properties").Effect]} ${access[e.data("properties").Access]}`,
                'control-point-step-size': '50',
                'width': '1px',
                'label': 'data (name)',
                'color': 'Black',
                'font-size': '10px',
                'text-background-padding': '0px',
                'text-rotation': 'autorotate',
                'text-background-color': 'White',
                'text-background-opacity': '1',
                'text-max-width': '1000px',
            }
        },
        {
            selector: 'edge.ACTION.Conditional',
            style: {
                'line-style': 'dashed',
            }
        },
        {
            selector: 'edge.ACTIONS',
            style: {
                "line-fill": "linear-gradient",
                'line-gradient-stop-colors': (e) => e.classes().filter(s => s in access).map(s => access[s]),
                'width': '1px',
                'label': 'data (name)',
                'font-weight': 'bold',
                'color': 'Black',
                'font-size': '10px',
                'text-background-padding': '0px',
                'text-rotation': 'autorotate',
                'text-background-color': 'White',
                'text-background-opacity': '1',
                'text-max-width': '1000px',
            }
        },
        {
            selector: 'node.selected',
            style: {
                'border-color': "black",
                'border-width': 1,
                'z-index': 4,
            }
        },
        {
            selector: 'edge.selected',
            style: {
                'z-index': 4,
                'width': '1.5px',
            }
        },

        {
            selector: '.unselected',
            style: {
                label: '',
                opacity: 0.1,
                zIndex: 0,
            }
        },
        {
            selector: 'edge.hover',
            style: {
                label: 'data (name)',
                textRotation: 0,
                textWrap: 'none',
                opacity: 1,
                zIndex: 10,
            }
        },

        {
            selector: 'node.hover',
            style: {
                label: 'data (name)',
                textWrap: 'none',
                height: 100,
                width: 100,
                opacity: 1,
                zIndex: 10,
            }
        },

        {
            selector: 'node.Generic',
            style: {
                label: '',
                borderStyle: "dashed",
                borderColor: "green",
                opacity: 0.7,
            }
        },
        {
            selector: 'node.expandible',
            style: {
                'background-image': (n) => badge(n, "collapsible")
            }
        },
        {
            selector: 'node.unexpandible',
            style: {
                borderColor: "silver",
                borderWidth: 2,
            }
        },
        {
            selector: 'node.collapsible',
            style: {
                'background-image': (n) => badge(n, "expandible")
            }
        },
        {
            selector: 'node.context-menu',
            style: {
                label: "",
            }
        },
        ],

        layout: {
            name: 'dagre',
            nodeSep: undefined,
            edgeSep: undefined,
            rankSep: undefined,
            rankDir: 'BT',
            ranker: undefined,
            minLen: function (edge) { return 1; },
            edgeWeight: function (edge) { return 1; },
            fit: true,
            padding: 40,
            spacingFactor: 1.5,
            nodeDimensionsIncludeLabels: true,
            animate: true,
            animateFilter: function (node, i) { return true; },
            animationDuration: 250,
            animationEasing: undefined,
            boundingBox: undefined,
            transform: function (node, pos) { return pos; },
            ready: function () { },
            stop: function () { }
        },
    },
}
