var leds = [];

// leds are formated like row_col
function clickOnDot(i, j) {
  var led = i + "_" + j
  if (leds.includes(led) == true) {
    leds = removeItemOnce(leds, led);
    turnLedOff(led);
  } else {
    leds.push(led);
    turnLedOn(led)
  }
  redrawTextArea();
}

function redrawTextArea() {
    document.getElementById("textarea").value = "";

    document.getElementById("textarea").value += "[";

    for (var k = 0; k < leds.length; k++) {
        led_arr = leds[k].split("_");
        document.getElementById("textarea").value += "(" + led_arr[0] + ", " + led_arr[1] + ")";

        if (!(k == leds.length - 1)) {
            document.getElementById("textarea").value += ", ";
        }
    }

    document.getElementById("textarea").value += "]" + "\n";
}

function removeItemOnce(arr, value) {
  var index = arr.indexOf(value);
  if (index > -1) {
    arr.splice(index, 1);
  }
  return arr;
}

function turnLedOff(led) {
    document.getElementById(led).style.fill = "#808080";
}

function turnLedOn(led) {
    document.getElementById(led).style.fill = "#FF0000";
}

function clearAllLeds() {
    for (var k = 0; k < leds.length; k++) {
        turnLedOff(leds[k]);
    }

    leds = [];

    redrawTextArea();
}

function copy() {
  let textarea = document.getElementById("textarea");
  textarea.select();
  document.execCommand("copy");
}

function update() {
  let text = document.getElementById("textarea").value;
  console.log(text);
  clearAllLeds(); // otherwise we will register allready on leds as being clicked off

  let regexp = /[^\d]*(\d+), (\d+)[^\d]*/;

  try {
      text_lst = text.split('), (')

      for (var k = 0; k < text_lst.length; k++) {
        dots = text_lst[k].match(regexp);
        console.log(dots);
        clickOnDot(dots[1], dots[2]);
      }
  } catch(err) {
    console.log('Could not regex parse input: ' + err.message);
  }
}