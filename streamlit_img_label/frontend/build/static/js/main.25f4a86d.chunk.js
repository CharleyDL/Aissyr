;(this.webpackJsonpstreamlit_img_label =
    this.webpackJsonpstreamlit_img_label || []).push([
    [0],
    {
        14: function (e, t, a) {
            e.exports = a(30)
        },
        27: function (e, t) {},
        28: function (e, t) {},
        29: function (e, t) {},
        30: function (e, t, a) {
            "use strict"
            a.r(t)
            var n = a(4),
                c = a.n(n),
                r = a(12),
                o = a.n(r),
                i = a(1),
                s = a(3),
                d = a(2),
                l = a(10),
                f = a(8),
                u = a(6),
                m = a.n(u),
                b = Object(l.b)(function (e) {
                    var t,
                        a = Object(n.useState)("light"),
                        r = Object(d.a)(a, 2),
                        o = r[0],
                        u = r[1],
                        b = Object(n.useState)([]),
                        h = Object(d.a)(b, 2),
                        g = h[0],
                        k = h[1],
                        v = Object(n.useState)(new f.fabric.Canvas("")),
                        j = Object(d.a)(v, 2),
                        O = j[0],
                        w = j[1],
                        p = e.args,
                        E = p.canvasWidth,
                        C = p.canvasHeight,
                        R = p.imageData,
                        x = Object(n.useState)(0),
                        S = Object(d.a)(x, 2),
                        _ = S[0],
                        L = S[1],
                        N = document.createElement("canvas"),
                        I = N.getContext("2d")
                    if (((N.width = E), (N.height = C), I)) {
                        var W = I.createImageData(E, C)
                        W.data.set(R),
                            I.putImageData(W, 0, 0),
                            (t = N.toDataURL())
                    } else t = ""
                    Object(n.useEffect)(
                        function () {
                            var a = e.args,
                                n = a.rects,
                                c = a.boxColor,
                                r = new f.fabric.Canvas("c", {
                                    enableRetinaScaling: !1,
                                    backgroundImage: t,
                                    uniScaleTransform: !0,
                                })
                            n.forEach(function (e) {
                                var t = e.top,
                                    a = e.left,
                                    n = e.width,
                                    o = e.height
                                r.add(
                                    new f.fabric.Rect({
                                        left: a,
                                        top: t,
                                        fill: "",
                                        width: n,
                                        height: o,
                                        objectCaching: !0,
                                        stroke: c,
                                        strokeWidth: 1,
                                        strokeUniform: !0,
                                        hasRotatingPoint: !1,
                                    })
                                )
                            }),
                                k(
                                    n.map(function (e) {
                                        return e.label
                                    })
                                ),
                                w(r),
                                l.a.setFrameHeight()
                        },
                        [C, E, t]
                    )
                    var y = function () {
                            L(0),
                                O.getObjects().forEach(function (e) {
                                    return O.remove(e)
                                }),
                                D([])
                        },
                        D = function (e) {
                            k(e)
                            var t = O.getObjects().map(function (t, a) {
                                return Object(s.a)(
                                    Object(s.a)({}, t.getBoundingRect()),
                                    {},
                                    { label: e[a] }
                                )
                            })
                            l.a.setComponentValue({ rects: t })
                        }
                    Object(n.useEffect)(function () {
                        if (O) {
                            return (
                                O.on("object:modified", function () {
                                    O.renderAll(), D(g)
                                }),
                                function () {
                                    O.off("object:modified")
                                }
                            )
                        }
                    })
                    var M = function (e) {
                        u(e),
                            "dark" === e
                                ? document.body.classList.add("dark-mode")
                                : document.body.classList.remove("dark-mode")
                    }
                    return (
                        Object(n.useEffect)(function () {
                            return (
                                window
                                    .matchMedia("(prefers-color-scheme: dark)")
                                    .addEventListener("change", function (e) {
                                        return M(e.matches ? "dark" : "light")
                                    }),
                                M(
                                    window.matchMedia(
                                        "(prefers-color-scheme: dark)"
                                    ).matches
                                        ? "dark"
                                        : "light"
                                ),
                                function () {
                                    window
                                        .matchMedia(
                                            "(prefers-color-scheme: dark)"
                                        )
                                        .removeEventListener(
                                            "change",
                                            function () {}
                                        )
                                }
                            )
                        }, []),
                        c.a.createElement(
                            c.a.Fragment,
                            null,
                            c.a.createElement("canvas", {
                                id: "c",
                                className: "dark" === o ? m.a.dark : "",
                                width: E,
                                height: C,
                            }),
                            c.a.createElement(
                                "div",
                                { className: "dark" === o ? m.a.dark : "" },
                                c.a.createElement(
                                    "button",
                                    {
                                        className: "dark" === o ? m.a.dark : "",
                                        onClick: function () {
                                            var t = {
                                                left: 0.15 * E + 3 * _,
                                                top: 0.15 * C + 3 * _,
                                                width: 0.2 * E,
                                                height: 0.2 * C,
                                            }
                                            L(_ + 1),
                                                O.add(
                                                    new f.fabric.Rect(
                                                        Object(s.a)(
                                                            Object(s.a)({}, t),
                                                            {},
                                                            {
                                                                fill: "",
                                                                objectCaching:
                                                                    !0,
                                                                stroke: e.args
                                                                    .boxColor,
                                                                strokeWidth: 1,
                                                                strokeUniform:
                                                                    !0,
                                                                hasRotatingPoint:
                                                                    !1,
                                                            }
                                                        )
                                                    )
                                                ),
                                                D(
                                                    [].concat(Object(i.a)(g), [
                                                        "",
                                                    ])
                                                )
                                        },
                                    },
                                    "Add bounding box"
                                ),
                                c.a.createElement(
                                    "button",
                                    {
                                        className: "dark" === o ? m.a.dark : "",
                                        onClick: function () {
                                            var e = O.getActiveObject(),
                                                t = O.getObjects().indexOf(e)
                                            O.remove(e),
                                                D(
                                                    g.filter(function (e, a) {
                                                        return a !== t
                                                    })
                                                )
                                        },
                                    },
                                    "Remove select"
                                ),
                                c.a.createElement(
                                    "button",
                                    {
                                        className: "dark" === o ? m.a.dark : "",
                                        onClick: function () {
                                            y()
                                            var t = e.args,
                                                a = t.rects,
                                                n = t.boxColor
                                            a.forEach(function (e) {
                                                var t = e.top,
                                                    a = e.left,
                                                    c = e.width,
                                                    r = e.height
                                                O.add(
                                                    new f.fabric.Rect({
                                                        left: a,
                                                        top: t,
                                                        fill: "",
                                                        width: c,
                                                        height: r,
                                                        objectCaching: !0,
                                                        stroke: n,
                                                        strokeWidth: 1,
                                                        strokeUniform: !0,
                                                        hasRotatingPoint: !1,
                                                    })
                                                )
                                            }),
                                                D(g)
                                        },
                                    },
                                    "Reset"
                                ),
                                c.a.createElement(
                                    "button",
                                    {
                                        className: "dark" === o ? m.a.dark : "",
                                        onClick: y,
                                    },
                                    "Clear all"
                                )
                            )
                        )
                    )
                })
            o.a.render(
                c.a.createElement(
                    c.a.StrictMode,
                    null,
                    c.a.createElement(b, null)
                ),
                document.getElementById("root")
            )
        },
        6: function (e, t, a) {
            e.exports = { dark: "StreamlitImgLabel_dark__PyW4C" }
        },
    },
    [[14, 1, 2]],
])
