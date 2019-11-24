//Dont change it
//Dont change it
requirejs(['ext_editor_io', 'jquery_190', 'raphael_210'],
    function (extIO, $) {
        function inscribeCanvas(dom, data) {

            if (! data || ! data.ext) {
                return
            }

            const input = data.in[0]
            const explanation = data.ext.explanation

            /*----------------------------------------------*
             *
             * attr
             *
             *----------------------------------------------*/
            const BG_COLOR = '#dfe8f7'
            const attr = {
                line: {
                    axis: {
                        'stroke-width': '0.5px',
                        'arrow-end': 'block-wide-long',
                    },
                    scale: {
                        'stroke-width': '0.5px',
                    }
                },
                rectangle: {
                    'stroke-width': '0px',
                    'fill': '#8fc7ed',
                },
                text: {
                    normal: {
                        'fill': 'black',
                    },
                    red: {
                        'fill': 'red',
                    },
                    scale_v: {
                        'text-anchor': 'end',
                    },
                },
                circle: {
                    normal: {
                        'stroke': 'black',
                        'fill': 'black',
                    },
                    red: {
                        'stroke': 'red',
                        'fill': 'red',
                    },
                },
            }

            /*----------------------------------------------*
             *
             * paper
             *
             *----------------------------------------------*/
            const [OS_L, OS_R, OS_T, OS_B] = [30, 30, 20, 20]
            const GRAPH_SIZE = 300

            let max_coord = 0
            let min_coord = 99999
            for (const [x, y] of [...input, ...explanation]) {
                max_coord = Math.max(max_coord, x, y)
                min_coord = Math.min(min_coord, x, y)
            }

            const grain = max_coord - min_coord <= 10 ? 5 : 50
            const positive_scale = Math.ceil(Math.max(0, max_coord) / grain) * grain
            const negative_scale = Math.floor(Math.min(0, min_coord) / grain) * grain * -1
            const all_scale = positive_scale + negative_scale

            const ratio = GRAPH_SIZE / all_scale

            const paper = Raphael(dom, GRAPH_SIZE+OS_L+OS_R, GRAPH_SIZE+OS_T+OS_B, 0, 0);

            /*----------------------------------------------*
             *
             * rectangle
             *
             *----------------------------------------------*/
            let path = []
            explanation.forEach(([x, y], i) => {
                path = [...path, (i == 0 ? 'M' : 'L'),
                        OS_L+(x+negative_scale)*ratio,
                        OS_T+(positive_scale-y)*ratio]
            })

            paper.path([...path, 'Z']).attr(attr.rectangle)

            /*----------------------------------------------*
             *
             * scale
             *
             *----------------------------------------------*/
            // axis
            paper.path(['M', OS_L, OS_T+positive_scale*ratio,
                        'h', GRAPH_SIZE+10]).attr(attr.line.axis)
            paper.path(['M', OS_L+negative_scale*ratio, OS_T+GRAPH_SIZE,
                        'v', -GRAPH_SIZE-10]).attr(attr.line.axis)

            // origin
            paper.text(OS_L+negative_scale*ratio-10,
                        OS_T+positive_scale*ratio+10, 0)

            // figure
            let figures = []
            if (positive_scale <= 10) {
                figures = [-10, -5, 5, 10]
            } else if (positive_scale <= 100) {
                figures = [-100, -50, 50, 100]
            } else {
                let h = Math.floor(positive_scale / 100) * -100
                while (h <= positive_scale) {
                    if (h != 0) {
                        figures.push(h)
                    }
                    h += 100
                }
            }

            for (const n of figures) {
                if (n >= -negative_scale) {
                    // h
                    paper.path(['M', OS_L+(n+negative_scale)*ratio,
                                OS_T+positive_scale*ratio, 'v', 3]).attr(attr.line.scale)
                    paper.text(OS_L+(n+negative_scale)*ratio,
                                OS_T+positive_scale*ratio+10, n)
                    // v
                    paper.path(['M', OS_L+(negative_scale)*ratio,
                                OS_T+(positive_scale-n)*ratio, , 'h', -3]).attr(attr.line.scale)
                    paper.text(OS_L+(negative_scale)*ratio-5,
                                OS_T+(positive_scale-n)*ratio, n).attr(attr.text.scale_v)
                }
            }

            /*----------------------------------------------*
             *
             * plot
             *
             *----------------------------------------------*/
            for (const [x, y] of input) {
                paper.circle(OS_L+(x+negative_scale)*ratio,
                                OS_T+(positive_scale-y)*ratio, 1).attr(
                                    attr.circle.normal)
            }

            /*----------------------------------------------*
             *
             * corner
             *
             *----------------------------------------------*/
            explanation.forEach(([x, y], i) => {
                const is_plot = input.some(([ix, iy])=>x == ix && y == iy)

                paper.text(OS_L+(x+negative_scale)*ratio,
                            OS_T+(positive_scale-y)*ratio-10,
                            '('+x+', '+y+')').attr(
                                    is_plot ? attr.text.normal
                                            : attr.text.red)
                if (! is_plot) {
                    paper.circle(OS_L+(x+negative_scale)*ratio,
                                    OS_T+(positive_scale-y)*ratio,
                                    1).attr(attr.circle.red)
                }
            })
        }

        var $tryit;

        var io = new extIO({
            multipleArguments: true,
            functions: {
                python: 'inscribe',
                js: 'inscribe'
            },
            animation: function($expl, data){
                inscribeCanvas(
                    $expl[0],
                    data,
                );
            }
        });
        io.start();
    }
);
