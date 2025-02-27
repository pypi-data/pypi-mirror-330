import os
import colorsys
import importlib
import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np


def showSwatch(swatch, M=6):
    fig = plt.figure(figsize=(9, 4), dpi=216)
    ax = fig.add_axes([0, 0, 1, 0.92], frameon=False)
    for i in range(42):
        x = i % M
        y = M - i // M
        c = swatch[i]
        # print('{0:.2f},{1:.2f} -> {2}'.format(x, y, c[1].hex_format()))
        plt.plot(x, y, ".", markersize=50, color=c[1].hex_format())
        plt.text(x + 0.004, y - 0.03, str(i), color="white", va="center", ha="center")
        plt.text(x + 0.15, y - 0.03, c[0], va="center")
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_xlim([-0.15, M])
    ax.set_ylim([-0.5, M + 0.5])
    fig.suptitle("Swatch", fontweight="bold")
    return fig


def rgb2lab(rgb):
    rgbv = np.array(rgb) / 255.0
    if len(rgbv.shape) == 1:
        rgbv = rgbv[(np.newaxis)]
    matrix = [[0.412453, 0.357580, 0.180423], [0.212671, 0.715160, 0.072169], [0.019334, 0.119193, 0.950227]]
    mat = np.array(matrix).transpose()
    xyz = np.matmul(rgbv, mat)
    # Normalize to D65 white point
    x = xyz[:, 0] / 0.950456
    y = xyz[:, 1]
    z = xyz[:, 2] / 1.088754
    # Threshold
    T = 0.008856
    xt = (x > T).astype(bool)
    yt = (y > T).astype(bool)
    zt = (z > T).astype(bool)
    y3 = y ** (1.0 / 3.0)
    fX = np.multiply(xt, x ** (1.0 / 3.0)) + np.multiply(~xt, 7.787 * x + 16.0 / 116.0)
    fY = np.multiply(yt, y3) + np.multiply(~yt, 7.787 * y + 16.0 / 116.0)
    fZ = np.multiply(zt, z ** (1.0 / 3.0)) + np.multiply(~zt, 7.787 * y + 16.0 / 116.0)
    L = np.multiply(yt, 116.0 * y3 - 16.0) + np.multiply(~yt, 903.3 * y)
    a = 500.0 * (fX - fY)
    b = 200.0 * (fY - fZ)
    return np.array([L, a, b]).transpose()


def listFonts(verbose=0, showname=False):
    def _html(fontname, showname=showname):
        line = f'<p><span style="font-family:{fontname}; font-size:16pt;">{fontname}</span>'
        if showname:
            line += f' (<span style="color:blue;">{fontname}</span>)'
        line += "</p>"
        return line

    font_path = "fonts"
    if os.path.exists(font_path):
        font_files = fm.findSystemFonts(fontpaths=[font_path])
        font_names = fm.createFontList(font_files)
        fm.fontManager.ttflist.extend(font_names)
    code = "\n".join([_html(font) for font in sorted(set([f.name for f in fm.fontManager.ttflist]))])
    if verbose:
        print("Type these in Notebook:\nfrom IPython.core.display import HTML\nHTML(result)")
    html = '<div style="column-count:2;">{}</div>'.format(code)
    return html


def colorspace(rgba):
    # Some constants for convenient coding later
    count = len(rgba)
    x = np.arange(count)
    rgba = np.array(rgba)
    rgb = rgba[:, :3]

    # Color in HSV representation
    hsv = np.array([colorsys.rgb_to_hsv(r, g, b) for r, g, b in rgb])

    # If image width = 1280, 0.8 x 1280 = 1024
    BACK_RECT = [0.1, 0.11, 0.8, 0.85]
    LINE_RECT = [0.1, 0.41, 0.8, 0.55]
    MAIN_RECT = [0.1, 0.11, 0.8, 0.30]

    linewidth = 1.5

    # New figure
    fig = plt.figure(figsize=(8.8889, 5), dpi=144)
    fig.patch.set_alpha(0.0)

    # Background
    axb = fig.add_axes(BACK_RECT, frameon=False)
    axb.yaxis.set_visible(False)
    axb.xaxis.set_visible(False)

    # Main axis for images
    axm = fig.add_axes(MAIN_RECT, label="Images")
    axm.patch.set_visible(False)

    # Line axis for lines
    axl = fig.add_axes(LINE_RECT, label="Lines")
    axl.patch.set_visible(False)
    axl.xaxis.set_visible(False)

    # Draw
    if count <= 64:
        marker = "."
    else:
        marker = None
    line_r = matplotlib.lines.Line2D(x, rgb[:, 0], linewidth=linewidth, color="r", label="R", marker=marker)
    line_g = matplotlib.lines.Line2D(x, rgb[:, 1], linewidth=linewidth, color="g", label="G", marker=marker)
    line_b = matplotlib.lines.Line2D(x, rgb[:, 2], linewidth=linewidth, color="b", label="B", marker=marker)
    line_h = matplotlib.lines.Line2D(x, hsv[:, 0], linewidth=linewidth, color=(0.0, 0.6, 0.7), label="H", marker=marker)
    line_s = matplotlib.lines.Line2D(x, hsv[:, 1], linewidth=linewidth, color=(1.0, 0.7, 0.2), label="S", marker=marker)
    line_v = matplotlib.lines.Line2D(x, hsv[:, 2], linewidth=linewidth, color=(0.3, 0.3, 0.3), label="V", marker=marker)
    axl.add_line(line_v)
    axl.add_line(line_s)
    axl.add_line(line_h)
    axl.add_line(line_b)
    axl.add_line(line_g)
    axl.add_line(line_r)
    if rgba.shape[1] > 3:
        line_a = matplotlib.lines.Line2D(
            x, rgba[:, 3], linewidth=linewidth, color="#777777", label="A", marker=marker, linestyle=":"
        )
        axl.add_line(line_a)

    # Backdrop gradient
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list("backdrop", rgb)
    axb.imshow(np.arange(count).reshape(1, -1), cmap=cmap, extent=(0, 1, 0, 1), aspect="auto", alpha=0.2)

    # Various representations of the colors
    clr = np.expand_dims(rgb, axis=0)
    red = np.zeros((1, count, 3))
    red[0, :, 0] = rgb[:, 0]
    grn = np.zeros((1, count, 3))
    grn[0, :, 1] = rgb[:, 1]
    blu = np.zeros((1, count, 3))
    blu[0, :, 2] = rgb[:, 2]
    c = plt.get_cmap("hsv")
    hue = np.expand_dims(np.array([c(i)[:3] for i in hsv[:, 0]]), axis=0)
    c = plt.get_cmap("Purples")
    sat = np.expand_dims(np.array([c(i)[:3] for i in hsv[:, 1]]), axis=0)
    c = plt.get_cmap("gray")
    val = np.expand_dims(np.array([c(i)[:3] for i in hsv[:, 2]]), axis=0)
    # Lower image to show various color components / intrinsic parameters
    if rgba.shape[1] > 3:
        alp = np.expand_dims(np.array([c(i)[:3] for i in rgba[:, 3]]), axis=0)
        img = np.concatenate((clr, red, grn, blu, hue, sat, val, alp), axis=0)
        axm.imshow(img, extent=(-0.5, count - 0.5, -0.5, 7.5), aspect="auto")
        axl.set_title("Color Space - RGB, HSV, A", weight="bold")
        axm.set_yticks(range(8))
        _ = axm.set_yticklabels(["Opacity", "Value", "Saturation", "Hue", "Blue", "Green", "Red", "Swatch"])
        lines = [line_r, line_g, line_b, line_h, line_s, line_v, line_a]
        _ = axl.legend(handles=lines, loc="upper left", ncol=7, frameon=False, fontsize=9)
    else:
        img = np.concatenate((clr, red, grn, blu, hue, sat, val), axis=0)
        axm.imshow(img, extent=(-0.5, count - 0.5, -0.5, 6.5), aspect="auto")
        axl.set_title("Color Space - RGB, HSV", weight="bold")
        axm.set_yticks(range(7))
        _ = axm.set_yticklabels(["Value", "Saturation", "Hue", "Blue", "Green", "Red", "Swatch"])
        lines = [line_r, line_g, line_b, line_h, line_s, line_v]
        _ = axl.legend(handles=lines, loc="upper left", ncol=6, frameon=False, fontsize=9)

    # Axis limits, grid, etc.
    axl.set_xlim([-0.5, count - 0.5])
    axl.set_ylim([-0.05, 1.18])
    axl.set_ylabel("Values")
    axl.grid(alpha=0.5, color="k", linestyle=":")
    axm.set_xlabel("Color Index")
    if count <= 32:
        axm.set_xticks(range(count))


def showLineColors(N=10):
    plt.plot(range(N) + 0.5 * (np.random.random((10, N)) - 0.5), "-o")
    plt.grid()


def showFontWeights(name="Helvetica Neue", color=None):
    fontnames = [x.name for x in fm.fontManager.ttflist]
    weight_names = [
        "ultralight",
        "light",
        "book",
        "normal",
        "regular",
        "medium",
        "roman",
        "demi",
        "semibold",
        "bold",
        "heavy",
        "extra bold",
        "black",
    ]
    weights = [100, 200, 300, 400, 500, 600, 700, 800, 900]

    print(f"{name} in TTF collection: {name in fontnames}")

    N = max(len(weights), len(weight_names))
    c = {
        "font.family": "sans-serif",
        "font.sans-serif": [name, "Helvetica", "Arial", "DejaVu Sans"],
    }
    with plt.rc_context(c):
        dpi = 72
        height = 42
        pixels = (800, N * height)
        figsize = (pixels[0] / dpi, pixels[1] / dpi)
        plt.figure(figsize=figsize, dpi=dpi, frameon=False)
        ax = plt.axes([0, 0, 1, 1], snap=True)
        plt.axis("off")
        props = {"horizontalalignment": "left", "verticalalignment": "baseline", "fontsize": 28}
        if color is not None:
            props.update({"color": color})

        def _show_weights(ww, origin=5):
            o = origin / pixels[0]
            for i, w in enumerate(ww):
                y = (pixels[1] - props["fontsize"] - i * height) / pixels[1]
                t = ax.text(0, y, f"Bitcoin", family=name, weight=w, **props)
                e = t.get_window_extent()
                t.remove()
                _ = ax.text(o + 0.1, y, f"{name} {w}", family=name, weight=w, **props)
                y += 6 / pixels[1]
                _ = ax.text(o, y, f"{e.width:.2f}", family="monospace", fontsize=12)

        _show_weights(weights)
        _show_weights(weight_names, origin=405)


def getFontOfWeight(weight, prefix="NotoSans"):
    weight_names = ["Thin", "ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]
    fontpath = os.path.join(os.path.dirname(importlib.util.find_spec("blib").origin), "fonts")
    if isinstance(weight, int):
        index = min(max(weight // 100 - 1, 0), 8)
        name = f"{prefix}-{weight_names[index]}.ttf"
    else:
        name = f"{prefix}-{weight}.ttf"
    path = os.path.join(fontpath, name)
    if not os.path.exists(path):
        print(f"{path} not found")
        return None
    return fm.FontProperties(fname=path)


def showNotoSans(color=None):
    weights = ["Thin", "ExtraLight", "Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black"]

    N = len(weights)

    dpi = 72
    height = 42
    pixels = (800, N * height)
    figsize = (pixels[0] / dpi, pixels[1] / dpi)

    plt.figure(figsize=figsize, dpi=dpi, frameon=False)
    ax = plt.axes([0, 0, 1, 1], snap=True)
    plt.axis("off")

    props = {"horizontalalignment": "left", "verticalalignment": "baseline", "fontsize": 28}
    colors = [c["color"] for c in matplotlib.rcParams["axes.prop_cycle"]]
    if color is not None:
        props.update({"color": color})
    else:
        props.update({"color": colors[0]})

    for i, w in enumerate(weights):
        f = getFontOfWeight(w)
        y = (pixels[1] - 24 - i * height) / pixels[1]
        t = ax.text(0, y, f"Bitcoin", fontproperties=f, **props)
        e = t.get_window_extent()
        t.remove()
        _ = ax.text(0.1, y, f"Noto Sans {weights[i]}", fontproperties=f, **props)
        y += 6 / pixels[1]
        _ = ax.text(0, y, f"{e.width:.2f}", family="monospace", fontsize=12, color=colors[3])
