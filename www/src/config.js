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

export default {

    graph: {

        style: [{
            selector: 'node',
            style: {
                'font-family': 'Source Code Pro',
                'font-size': '12px',
                'height': 75,
                'width': 75,
                'label': 'data (name)',

                'background-color': 'white',
                'border-color': 'black',
                'border-width': 1,

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

                'font-family': 'Source Code Pro',
                'font-size': '8px',

                'curve-style': 'bezier',
                'target-arrow-shape': 'triangle',
                'width': '1px',

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
                    return n.data().type.split('::').reduce(
                        (o, i) => (i in o) ? o[i] : icons.AWS.Resource, icons);

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
                "line-fill": "radial-gradient",
                // Change to Allow & Deny + remaining action colors
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
            selector: '.selected',
            style: {
                'line-color': colors.blue.base,
                'line-gradient-stop-colors': colors.blue.base,
                'border-color': colors.blue.base,
                zIndex: 4,
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
            selector: 'node.collapsed',
            style: {
                borderStyle: "double",
                borderWidth: 5,
            }
        },

        {
            selector: 'node.expanded',
            style: {
            }
        },

        {
            selector: 'node.menu',
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
            animate: false,
            animateFilter: function (node, i) { return true; },
            animationDuration: 200,
            animationEasing: undefined,
            boundingBox: undefined,
            transform: function (node, pos) { return pos; },
            ready: function () { },
            stop: function () { }
        },
    },
}
