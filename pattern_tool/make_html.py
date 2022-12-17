# output control for embedded programming

definition = {
    "radius": 50,
    "gap": 10,
    "ux": 100,
    "uy": 100
}

size = 16

definition["rect_size"] = 2 * (definition["radius"] + definition["gap"]) * size

pattern = [["#808080" for i in range(0, size)] for j in range(0, size)]

with open('pattern_tool.html', 'w') as fh:
    fh.write("""<!DOCTYPE html>
<html>
<body>
<script src="state.js"></script>
<link rel="stylesheet" href="styles.css">

<div>
""")

    # start make display svg
    fh.write(f'<svg width="{600}px" height="{600}px" viewBox="100 100 2000 2000"')
    fh.write("""
    xmlns="http://www.w3.org/2000/svg" version="1.1">
    <desc>One 8x8 LED matrix</desc>


    <rect x="%(ux)i" y="%(uy)i" width="%(rect_size)i" height="%(rect_size)i"
        fill="black" stroke="black" stroke-width="0"/>""" % definition)

    dots = ""
    for i in range(0, size):
        for j in range(0, size):
            dots += """<circle id="%(id)s" cx="%(ux)i" cy="%(uy)i" r="%(radius)i" fill="%(color)s" stroke="black" onclick="%(onclick)s" stroke-width="0"  />\n""" % {
                "ux": definition["ux"] + (j + 1 / 2) * 2 * (definition["radius"] + definition["gap"]),
                "uy": definition["uy"] + (i + 1 / 2) * 2 * (definition["radius"] + definition["gap"]),
                "radius": definition["radius"],
                "color": pattern[j][i],
                "onclick": "clickOnDot(" + str(i + 1) + ", " + str(j + 1) + ")",
                "id": str(i + 1) + "_" + str(j + 1)
            }
    dots += "</svg>"
    fh.write(dots)
    # end make display svg
    fh.write("""
<div>
    <textarea id="textarea" " rows="4" cols="50"></textarea>
    <div id="btns">
        <button id="btn-update" onclick="update()">update</button>
        <button id="btn-clear" onclick="clearAllLeds()">clear all</button>
        <button id="btn-copy" onclick="copy()">copy</button>
    </div>
</div>
    """)
    fh.write("</div></body></html>")