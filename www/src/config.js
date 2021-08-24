import icons from './icons.js'
import colors from 'vuetify/lib/util/colors'

export const access = {
    "Allow": colors.green.base,
    "Deny": colors.red.base,
    "List": colors.yellow.base,
    "Permissions Management": colors.deepPurple.darken1,
    "Read": colors.pink.darken1,
    "Tagging": colors.teal.darken1,
    "Write": colors.indigo.darken2,
}

export const size = {
    "ACTION": 1,
    "ACTIONS": 1,
    "ADMIN": 3,
    "ATTACK": 1,
    "TRANSITIVE": 2,
    "TRUSTS": 1,
    'ASSOCIATIVE': 1,
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
                'background-color': 'white',
                'border-color': 'black',
                'border-width': 0.2,
                'color': 'white',
                'font-family': 'Roboto Mono, monospace',
                'font-size': '12px',
                'height': 75,
                'label': 'data (name)',
                'text-background-color': 'black',
                'text-background-opacity': '1',
                'text-background-padding': '2px',
                'text-background-shape': 'roundrectangle',
                'text-halign': 'center',
                'text-max-width': '160px',
                'text-valign': 'bottom',
                'text-wrap': 'ellipsis',
                'width': 75
            }
        },
        {
            selector: 'edge',
            style: {
                'curve-style': 'bezier',
                'font-family': 'Roboto Mono, monospace',
                'font-size': '10x',
                'font-size': 0,
                'line-color': "#999999",
                'target-arrow-color': "#999999",
                'target-arrow-shape': 'triangle',
                'text-max-width': '50px',
                'text-rotation': 0,
                'text-wrap': 'ellipsis',
                'width': function (e) {
                    return e.classes().filter(c =>
                        Object.keys(size).includes(c)
                    ).map(c => size[c]).concat(1)[0]
                },
                'z-index': '3'
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
            selector: function (e) {
                return (e.classes().includes("TRANSITIVE") &&
                    Object.keys(e.source().data("properties")
                    ).includes("PermissionsBoundary"))
            },
            style: {
                'line-style': 'dashed'
            }
        },
        {
            selector: 'edge.ASSOCIATIVE',
            style: {
                'line-style': 'dotted',
                'target-arrow-shape': 'none'
            }
        },
        {
            selector: 'edge.ATTACK',
            style: {
                'line-color': 'maroon',
                'line-style': 'dashed',
            }
        },
        {
            selector: 'edge.TRUSTS',
            style: {
                'color': 'black',
                'font-size': '10px',
                'line-color': 'gold',
                'text-background-color': 'white',
                'text-background-opacity': '1',
                'text-max-width': '1000px',
                'text-rotation': 'autorotate'
            }
        },
        {
            selector: 'edge.ACTION',
            style: {
                "line-fill": "linear-gradient",
                'color': 'black',
                'control-point-step-size': '50',
                'font-size': '10px',
                'label': 'data (name)',
                'line-gradient-stop-colors': function (e) {
                    return `${access[e.data("properties").Effect]}`
                        .concat(" ")
                        .concat(`${access[e.data("properties").Access]}`);
                },
                'target-arrow-color': (e) => `${access[e.data("properties").Access]}`,
                'text-background-color': 'white',
                'text-background-opacity': '1',
                'text-background-padding': '0px',
                'text-max-width': '1000px',
                'text-rotation': 'autorotate',
            }
        },
        {
            selector: 'edge.ACTION.Conditional',
            style: {
                'line-style': 'dashed'
            }
        },
        {
            selector: 'edge.ACTIONS',
            style: {
                "line-fill": "linear-gradient",
                'color': 'black',
                'font-size': '10px',
                'font-weight': 'bold',
                'label': 'data (name)',
                'line-gradient-stop-colors': (e) => e.classes().filter(s => s in access).map(s => access[s]),
                'text-background-color': 'White',
                'text-background-opacity': '1',
                'text-background-padding': '0px',
                'text-max-width': '1000px',
                'text-rotation': 'autorotate'
            }
        },
        {
            selector: 'edge.ADMIN',
            style: {
                'opacity': '0.4',
                'overlay-color': 'white',
                'overlay-padding': '1px',
                'overlay-opacity': '1px',
                'target-arrow-shape': 'chevron',
                'target-arrow-fill': 'filled',
                'color': 'black',
            }
        },
        {
            selector: 'node.selected',
            style: {
                'border-color': "black",
                'border-width': 1,
                'z-index': 4
            }
        },
        {
            selector: 'edge.selected',
            style: {
                'opacity': '1',
                'width': function (e) {
                    const scale = 1.5;
                    return e.classes().filter(c =>
                        Object.keys(size).includes(c)
                    ).map(c => size[c] * scale).concat(scale)[0]
                },
                'z-index': 4,
            }
        },
        {
            selector: '.unselected',
            style: {
                'font-size': '0',
                'opacity': 0.1,
                'z-index': 0
            }
        },
        {
            selector: 'edge.hover',
            style: {
                'font-size': '10px',
                'font-weight': 'bold',
                'opacity': 1,
                'text-background-color': 'white',
                'text-background-opacity': '1',
                'text-max-width': '1000px',
                'text-rotation': 'autorotate',
                'text-rotation': 0,
                'text-wrap': 'none',
                'width': function (e) {
                    const scale = 1.75;
                    return e.classes().filter(c =>
                        Object.keys(size).includes(c)
                    ).map(c => size[c] * scale).concat(scale)[0]
                },
                'z-index': 10
            }
        },
        {
            selector: 'node.hover',
            style: {
                'font-size': '12px',
                'height': 100,
                'opacity': 1,
                'text-wrap': 'none',
                'width': 100,
                'z-index': 10
            }
        },
        {
            selector: 'node.Generic',
            style: {
                'border-color': "green",
                'border-style': "dashed",
                'label': '',
                'opacity': 0.7
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
                'border-color': "silver",
                'border-width': 2
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
                'label': ""
            }
        }],
        layout: {
            animate: true,
            animateFilter: function (node, i) { return true; },
            animationDuration: 250,
            animationEasing: undefined,
            boundingBox: undefined,
            edgeSep: undefined,
            edgeWeight: function (edge) { return 1; },
            fit: true,
            minLen: function (edge) { return 1; },
            name: 'dagre',
            nodeDimensionsIncludeLabels: true,
            nodeSep: undefined,
            padding: 40,
            rankDir: 'BT',
            rankSep: undefined,
            ranker: 'longest-path',
            ready: function () { },
            spacingFactor: 1.5,
            stop: function () { },
            transform: function (node, pos) { return pos; }
        },
    }
}
