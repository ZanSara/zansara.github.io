---
title: "Generating creatures with Teranoptia"
date: 2024-05-06
author: "ZanSara"
tags: [JS, JavaScript, Font, Fun, Regex, Grammar, "Computer Science"]
featuredImage: "/posts/2024-05-06-teranoptia/cover.png"
---

{{< raw >}}
<style>
    @font-face {
        font-family: teranoptia;
        src: url("/posts/2024-05-06-teranoptia/teranoptia/fonts/Teranoptia-Furiae.ttf");
    }

    .teranoptia {
        font-size: 5rem;
        font-family: teranoptia;
        hyphens: none!important;
        line-height: 70px;
    }

    .small {
        font-size:3rem;
        line-height: 40px;
    }

    .glyphset {
        display: flex;
        flex-wrap: wrap;
    }
    .glyphset div {
        margin: 3px;
    }
    .glyphset div p {
        text-align: center;
    }

</style>
{{< /raw >}}

Having fun with fonts doesn't always mean obsessing over kerning and ligatures. Sometimes, writing text is not even the point!

You don't believe it? Type something in here.

{{< raw >}}

<textarea id="test-generated-animal" class="teranoptia" style="width: 100%; line-height: 50pt;"></textarea>

<div style="display: flex; gap: 10px;">
    Characters to generate:
    <input id="test-glyph-count" type="number" value=10 ></input>
    <button onclick="generateTest(document.getElementById('test-glyph-count').value);">Generate!</button>
</div>

<script>
function makeBreakable(animal){
    // Line break trick - avoid hypens and allows wrapping
    const animalFragments = animal.split(/(?=[yvspmieaźACFILOSWŹv])/g);
    animal = animalFragments.join("<wbr>");
    return animal;
}

function generateTest(value){
    var newAnimal = '';
    for (var i = 0; i < value; i++) {
        newAnimal += randomFrom(validChars);
    }
    document.getElementById("test-generated-animal").value = newAnimal;
}

</script>
{{< /raw >}}

[Teranoptia](https://www.tunera.xyz/fonts/teranoptia/) is a cool font that lets you build small creatures by mapping each letter (and a few other characters) to a piece of a creature like a head, a tail, a leg, a wing and so on. By typing words you can create strings of creatures. 

Here is the glyphset:

{{< raw >}}
<div class="glyphset">
    <div><p>A</p><p class="teranoptia">A</p></div>

    <div><p>B</p><p class="teranoptia">B</p></div>

    <div><p>C</p><p class="teranoptia">C</p></div>

    <div><p>D</p><p class="teranoptia">D</p></div>

    <div><p>E</p><p class="teranoptia">E</p></div>

    <div><p>F</p><p class="teranoptia">F</p></div>

    <div><p>G</p><p class="teranoptia">G</p></div>

    <div><p>H</p><p class="teranoptia">H</p></div>

    <div><p>I</p><p class="teranoptia">I</p></div>

    <div><p>J</p><p class="teranoptia">J</p></div>

    <div><p>K</p><p class="teranoptia">K</p></div>

    <div><p>L</p><p class="teranoptia">L</p></div>

    <div><p>M</p><p class="teranoptia">M</p></div>

    <div><p>N</p><p class="teranoptia">N</p></div>

    <div><p>O</p><p class="teranoptia">O</p></div>

    <div><p>P</p><p class="teranoptia">P</p></div>

    <div><p>Q</p><p class="teranoptia">Q</p></div>

    <div><p>R</p><p class="teranoptia">R</p></div>

    <div><p>S</p><p class="teranoptia">S</p></div>

    <div><p>T</p><p class="teranoptia">T</p></div>

    <div><p>U</p><p class="teranoptia">U</p></div>

    <div><p>V</p><p class="teranoptia">V</p></div>

    <div><p>W</p><p class="teranoptia">W</p></div>

    <div><p>X</p><p class="teranoptia">X</p></div>

    <div><p>Ẋ</p><p class="teranoptia">Ẋ</p></div>

    <div><p>Y</p><p class="teranoptia">Y</p></div>

    <div><p>Z</p><p class="teranoptia">Z</p></div>

    <div><p>Ź</p><p class="teranoptia">Ź</p></div>

    <div><p>Ž</p><p class="teranoptia">Ž</p></div>

    <div><p>Ż</p><p class="teranoptia">Ż</p></div>

    <div><p>a</p><p class="teranoptia">a</p></div>

    <div><p>b</p><p class="teranoptia">b</p></div>

    <div><p>ḅ</p><p class="teranoptia">ḅ</p></div>

    <div><p>c</p><p class="teranoptia">c</p></div>

    <div><p>d</p><p class="teranoptia">d</p></div>

    <div><p>e</p><p class="teranoptia">e</p></div>

    <div><p>f</p><p class="teranoptia">f</p></div>

    <div><p>g</p><p class="teranoptia">g</p></div>

    <div><p>h</p><p class="teranoptia">h</p></div>

    <div><p>i</p><p class="teranoptia">i</p></div>

    <div><p>j</p><p class="teranoptia">j</p></div>

    <div><p>k</p><p class="teranoptia">k</p></div>

    <div><p>l</p><p class="teranoptia">l</p></div>

    <div><p>m</p><p class="teranoptia">m</p></div>

    <div><p>n</p><p class="teranoptia">n</p></div>

    <div><p>o</p><p class="teranoptia">o</p></div>

    <div><p>p</p><p class="teranoptia">p</p></div>

    <div><p>q</p><p class="teranoptia">q</p></div>

    <div><p>r</p><p class="teranoptia">r</p></div>

    <div><p>s</p><p class="teranoptia">s</p></div>

    <div><p>t</p><p class="teranoptia">t</p></div>

    <div><p>u</p><p class="teranoptia">u</p></div>

    <div><p>v</p><p class="teranoptia">v</p></div>

    <div><p>w</p><p class="teranoptia">w</p></div>

    <div><p>x</p><p class="teranoptia">x</p></div>

    <div><p>y</p><p class="teranoptia">y</p></div>

    <div><p>z</p><p class="teranoptia">z</p></div>

    <div><p>ź</p><p class="teranoptia">ź</p></div>

    <div><p>ž</p><p class="teranoptia">ž</p></div>

    <div><p>ż</p><p class="teranoptia">ż</p></div>

    <div><p>,</p><p class="teranoptia">,</p></div>

    <div><p>*</p><p class="teranoptia">*</p></div>

    <div><p>(</p><p class="teranoptia">(</p></div>

    <div><p>)</p><p class="teranoptia">)</p></div>

    <div><p>{</p><p class="teranoptia">{</p></div>

    <div><p>}</p><p class="teranoptia">}</p></div>

    <div><p>[</p><p class="teranoptia">[</p></div>

    <div><p>]</p><p class="teranoptia">]</p></div>

    <div><p>‐</p><p class="teranoptia">‐</p></div>

    <div><p>“</p><p class="teranoptia">“</p></div>

    <div><p>”</p><p class="teranoptia">”</p></div>

    <div><p>‘</p><p class="teranoptia">‘</p></div>

    <div><p>’</p><p class="teranoptia">’</p></div>

    <div><p>«</p><p class="teranoptia">«</p></div>

    <div><p>»</p><p class="teranoptia">»</p></div>

    <div><p>‹</p><p class="teranoptia">‹</p></div>

    <div><p>›</p><p class="teranoptia">›</p></div>

    <div><p>$</p><p class="teranoptia">$</p></div>

    <div><p>€</p><p class="teranoptia">€</p></div>
</div>

You'll notice that there's a lot you can do with it, from assembling simple creatures:

<p class="teranoptia">vTN</p>

to more complex, multi-line designs:

<p class="teranoptia"><wbr> {Ž}</p>
<p class="teranoptia">F] [Z</p>

{{< /raw >}}

Let's play with it a bit and see how we can put together a few "correct" looking creatures.

{{< notice info >}}

_As you're about to notice, I'm no JavaScript developer. Don't expect high-quality JS in this post._

{{< /notice >}}

## Mirroring animals

To begin with, let's start with a simple function: animal mirroring. The glyphset includes a mirrored version of each non-symmetric glyph, but the mapping is rather arbitrary, so we are going to need a map.

Here are the pairs: 

<p class="small teranoptia" style="letter-spacing: 5px;"> By Ev Hs Kp Nm Ri Ve Za Żź Az Cx Fu Ir Lo Ol Sh Wd Źż vE Dw Gt Jq Mn Pk Qj Tg Uf Xc Ẋḅ Yb Žž bY cX () [] {} </p>

### Animal mirror

{{< raw >}}

<div style="display: flex; gap: 10px;">
    <input id="original-animal" type="text" class="teranoptia" style="width: 50%; text-align:right;" oninput="mirrorAnimal(this.value);" value="WYZ*p»gh"></input>
    <p id="mirrored-animal" class="teranoptia" style="line-height: 50pt;">ST»K*abd</p>
</div>

<script>
const mirrorPairs = {"B": "y",  "y": "B", "E": "v",  "v": "E", "H": "s",  "s": "H", "K": "p",  "p": "K", "N": "m",  "m": "N", "R": "i",  "i": "R", "V": "e",  "e": "V", "Z": "a",  "a": "Z", "Ż": "ź",  "ź": "Ż", "A": "z",  "z": "A", "C": "x",  "x": "C", "F": "u",  "u": "F", "I": "r",  "r": "I", "L": "o",  "o": "L", "O": "l",  "l": "O", "S": "h",  "h": "S", "W": "d",  "d": "W", "Ź": "ż",  "ż": "Ź", "v": "E",  "E": "v", "D": "w",  "w": "D", "G": "t",  "t": "G", "J": "q",  "q": "J", "M": "n",  "n": "M", "P": "k",  "k": "P", "Q": "j",  "j": "Q", "T": "g",  "g": "T", "U": "f",  "f": "U", "X": "c",  "c": "X", "Ẋ": "ḅ",  "ḅ": "Ẋ", "Y": "b",  "b": "Y", "Ž": "ž",  "ž": "Ž", "b": "Y",  "Y": "b", "c": "X",  "X": "c", "(": ")",  ")": "(", "[": "]",  "]": "[", "{": "}", "}": "{"};

function mirrorAnimal(original){
    var mirror = '';
    for (i = original.length-1; i >= 0; i--){
        newChar = mirrorPairs[original.charAt(i)];
        if (newChar){
            mirror += newChar;
        } else {
            mirror += original.charAt(i)
        }
        console.log(original, original.charAt(i), mirrorPairs[original.charAt(i)], mirror);
    }
    document.getElementById("mirrored-animal").innerHTML = mirror;
}
</script>
{{< /raw >}}

```javascript
const mirrorPairs = {"B": "y",  "y": "B", "E": "v",  "v": "E", "H": "s",  "s": "H", "K": "p",  "p": "K", "N": "m",  "m": "N", "R": "i",  "i": "R", "V": "e",  "e": "V", "Z": "a",  "a": "Z", "Ż": "ź",  "ź": "Ż", "A": "z",  "z": "A", "C": "x",  "x": "C", "F": "u",  "u": "F", "I": "r",  "r": "I", "L": "o",  "o": "L", "O": "l",  "l": "O", "S": "h",  "h": "S", "W": "d",  "d": "W", "Ź": "ż",  "ż": "Ź", "v": "E",  "E": "v", "D": "w",  "w": "D", "G": "t",  "t": "G", "J": "q",  "q": "J", "M": "n",  "n": "M", "P": "k",  "k": "P", "Q": "j",  "j": "Q", "T": "g",  "g": "T", "U": "f",  "f": "U", "X": "c",  "c": "X", "Ẋ": "ḅ",  "ḅ": "Ẋ", "Y": "b",  "b": "Y", "Ž": "ž",  "ž": "Ž", "b": "Y",  "Y": "b", "c": "X",  "X": "c", "(": ")",  ")": "(", "[": "]",  "]": "[", "{": "}", "}": "{"};

function mirrorAnimal(original){
    var mirror = '';
    for (i = original.length-1; i >= 0; i--){
        newChar = mirrorPairs[original.charAt(i)];
        if (newChar){
            mirror += newChar;
        } else {
            mirror += original.charAt(i)
        }
    }
    return mirror;
}
```


## Random animal generation

While it's fun to build complicated animals this way, you'll notice something: it's pretty hard to make them come out right by simply typing something. Most of the time you need quite careful planning. In addition there's almost no meaningful (English) word that corresponds to a well-defined creature. Very often the characters don't match, creating a sequence of "chopped" creatures.

For example, "Hello" becomes:

<p class="teranoptia">Hello</p>

This is a problem if we want to make a parametric or random creature generator, because most of the random strings won't look good. 

### Naive random generator

{{< raw >}}
<div style="display: flex; gap: 10px;">
    Characters to generate:
    <input id="naive-glyph-count" type="number" value=10></input>
    <button onclick="generateNaive(document.getElementById('naive-glyph-count').value);">Generate!</button>
</div>

<p id="naive-generated-animal" class="teranoptia" style="line-height: 50pt;">n]Zgameź)‐</p>

<script>
const validChars = "ABCDEFGHIJKLMNOPQRSTUVWXẊYZŹŽŻabḅcdefghijklmnopqrstuvwxyzźžż,*(){}[]‐“”«»$"; //‘’‹›€

function randomFrom(list){
    return list[Math.floor(Math.random() * list.length)];
}

function generateNaive(value){
    var newAnimal = '';
    for (var i = 0; i < value; i++) {
        newAnimal += randomFrom(validChars);
    }
    
    // Line break trick - helps with wrapping
    const animalFragments = newAnimal.split('');
    newAnimal = animalFragments.join("<wbr>");

    document.getElementById("naive-generated-animal").innerHTML = newAnimal;
}
generateNaive(document.getElementById('naive-glyph-count').value);

</script>
{{< /raw >}}

```javascript
const validChars = "ABCDEFGHIJKLMNOPQRSTUVWXẊYZŹŽŻabḅcdefghijklmnopqrstuvwxyzźžż,*(){}[]‐“”«»$"; // ‘’‹›€ excluded because they're mostly vertical

function randomFrom(list){
    return list[Math.floor(Math.random() * list.length)];
}

function generateNaive(value){
    var newAnimal = '';
    for (var i = 0; i < value; i++) {
        newAnimal += randomFrom(validChars);
    }
    return newAnimal;
}
```

Can we do better than this?

## Generating "good" animals

There are many ways to define "good" or "well-formed" creatures. One of the first rules we can introduce is that we don't want chopped body parts to float alone. 

Translating it into a rule we can implement: a character that is "open" on the right must be followed by a character that is open on the left, and a character that is _not_ open on the right must be followed by another character that is _not_ open on the left.

For example, <span class="small teranoptia">A</span> may be followed by <span class="small teranoptia">B</span> to make <span class="small teranoptia">AB</span>, but <span class="small teranoptia">A</span> cannot be followed by <span class="small teranoptia">C</span> to make <span class="small teranoptia">AC</span>. 

In the same way, <span class="small teranoptia">Z</span> may be followed by <span class="small teranoptia">A</span> to make <span class="small teranoptia">ZA</span>, but <span class="small teranoptia">Z</span> cannot be followed by <span class="small teranoptia">ż</span> to make <span class="small teranoptia">Zż</span>. 
 
This way we will get rid of all those "chopped" monsters that make up most of the randomly generated string.

To summarize, the rules we have to implement are:

- Any character that is open on the right must be followed by another character that is open on the left.
- Any character that is closed on the right must be followed by another character that is closed on the left.
- The first character must not be open on the left.
- The last character must not be open on the right.

### Non-chopped animals generator

{{< raw >}}
<div style="display: flex; gap: 10px;">
    Characters to generate:
    <input id="nochop-glyph-count" type="number" value=10></input>
    <button onclick="generateNoChop(document.getElementById('nochop-glyph-count').value);">Generate!</button>
</div>

<p id="nochop-generated-animal" class="teranoptia" style="line-height: 50pt;">suSHebQ«EIl</p>

<script>
const charsOpenOnTheRightOnly = "yvspmieaźACFILOSWŹ({[";
const charsOpenOnTheLeftOnly =  "BEHKNRVZŻzxurolhdż)]}";
const charsOpenOnBothSides = "DGJMPQTUXẊYŽbcwtqnkjgfcḅbžYX«»";
const charsOpenOnNoSides = ",*-“”";

const charsOpenOnTheRight = charsOpenOnTheRightOnly + charsOpenOnBothSides;
const charsOpenOnTheLeft = charsOpenOnTheLeftOnly + charsOpenOnBothSides;
const validInitialChars = charsOpenOnTheRightOnly + charsOpenOnNoSides;

function generateNoChop(value){
    document.getElementById("nochop-generated-animal").innerHTML = "";
    var newAnimal = '' + randomFrom(validInitialChars);
    for (var i = 0; i < value-1; i++) {
        if (charsOpenOnTheRight.indexOf(newAnimal[i]) > -1){
            newAnimal += randomFrom(charsOpenOnTheLeft);

        } else if (charsOpenOnTheLeftOnly.indexOf(newAnimal[i]) > -1){
            newAnimal += randomFrom(charsOpenOnTheRightOnly);
        
        } else if (charsOpenOnNoSides.indexOf(newAnimal[i]) > -1){
            newAnimal += randomFrom(validInitialChars);
        }
    }
    // Final character
    if (charsOpenOnTheRight.indexOf(newAnimal[i]) > -1){
        newAnimal += randomFrom(charsOpenOnTheLeftOnly);
    } else {
        newAnimal += randomFrom(charsOpenOnNoSides);
    }
    document.getElementById("nochop-generated-animal").innerHTML = makeBreakable(newAnimal);
}
generateNoChop(document.getElementById("nochop-glyph-count").value);

</script>
{{< /raw >}}

```javascript
const charsOpenOnTheRightOnly = "yvspmieaźACFILOSWŹ({[";
const charsOpenOnTheLeftOnly =  "BEHKNRVZŻzxurolhdż)]}";
const charsOpenOnBothSides = "DGJMPQTUXẊYŽbcwtqnkjgfcḅbžYX«»";
const charsOpenOnNoSides = ",*-“”";

const charsOpenOnTheRight = charsOpenOnTheRightOnly + charsOpenOnBothSides;
const charsOpenOnTheLeft = charsOpenOnTheLeftOnly + charsOpenOnBothSides;
const validInitialChars = charsOpenOnTheRightOnly + charsOpenOnNoSides;

function generateNoChop(value){
    var newAnimal = '' + randomFrom(validInitialChars);
    for (var i = 0; i < value-1; i++) {
        if (charsOpenOnTheRight.indexOf(newAnimal[i]) > -1){
            newAnimal += randomFrom(charsOpenOnTheLeft);

        } else if (charsOpenOnTheLeftOnly.indexOf(newAnimal[i]) > -1){
            newAnimal += randomFrom(charsOpenOnTheRightOnly);
        
        } else if (charsOpenOnNoSides.indexOf(newAnimal[i]) > -1){
            newAnimal += randomFrom(validInitialChars);
        }
    }
    // Final character
    if (charsOpenOnTheRight.indexOf(newAnimal[i]) > -1){
        newAnimal += randomFrom(charsOpenOnTheLeftOnly);
    } else {
        newAnimal += randomFrom(charsOpenOnNoSides);
    }
    return newAnimal;
}
```

The resulting animals are already quite better!

There are still a few things we may want to fix. For example, some animals end up being just a pair of heads (such as <span class="small teranoptia">sN</span>); others instead have their bodies oriented in the wrong direction (like <span class="small teranoptia">IgV</span>).

Let's try to get rid of those too.

The trick here is to separate the characters into two groups: elements that are "facing left", elements that are "facing right", and symmetric ones. At this point, it's convenient to call them "heads", "bodies" and "tails" to make the code more understandable, like the following:

- Right heads: <span class="small teranoptia">BEHKNRVZŻ</span>

- Left heads: <span class="small teranoptia">yvspmieaź</span>

- Right tails: <span class="small teranoptia">ACFILOSWŹv</span>

- Left tails: <span class="small teranoptia">zxurolhdżE</span>

- Right bodies: <span class="small teranoptia" style="letter-spacing: 5px;">DGJMPQTUẊŽ</span>

- Left bodies: <span class="small teranoptia" style="letter-spacing: 5px;">wtqnkjgfḅž</span>

- Entering hole: <span class="small teranoptia" style="letter-spacing: 5px;">)]}</span>

- Exiting hole: <span class="small teranoptia" style="letter-spacing: 5px;">([{</span>

- Bounce & symmetric bodies: <span class="small teranoptia" style="letter-spacing: 5px;">«»$bcXY</span>

- Singletons: <span class="small teranoptia" style="letter-spacing: 5px;">,*-</span>

Let's put this all together!

### Oriented animals generator

{{< raw >}}
<div style="display: flex; gap: 10px;">
    Characters to generate:
    <input id="oriented-glyph-count" type="number" value=10></input>
    <button onclick="generateOriented(document.getElementById('oriented-glyph-count').value);">Generate!</button>
</div>

<p id="oriented-generated-animal" class="teranoptia" style="line-height: 50pt;">suSHebQ«EIl</p>

<script>

const rightAnimalHeads = "BEHKNRVZŻ";
const leftAnimalHeads = "yvspmieaź";
const rightAnimalTails = "ACFILOSWŹv";
const leftAnimalTails = "zxurolhdżE";
const rightAnimalBodies = "DGJMPQTUẊŽ";
const leftAnimalBodies = "wtqnkjgfḅž";
const singletons = ",*‐";
const exitingHole = "([{";
const enteringHole = ")]}";
const bounce = "«»$bcXY";

const validStarts = leftAnimalHeads + rightAnimalTails + exitingHole;
const validSuccessors = {
    [exitingHole + bounce]: rightAnimalHeads + rightAnimalBodies + leftAnimalBodies + leftAnimalTails + enteringHole + bounce,
    [enteringHole]: rightAnimalTails + leftAnimalHeads + exitingHole + singletons,
    [rightAnimalHeads + leftAnimalTails + singletons]: rightAnimalTails + leftAnimalHeads + exitingHole + singletons,
    [leftAnimalHeads]: leftAnimalBodies + leftAnimalBodies + leftAnimalBodies + leftAnimalTails + enteringHole + bounce,
    [rightAnimalTails]: rightAnimalBodies + rightAnimalBodies + rightAnimalBodies + rightAnimalHeads + enteringHole + bounce,
    [rightAnimalBodies]: rightAnimalBodies + rightAnimalBodies + rightAnimalBodies + rightAnimalHeads + enteringHole + bounce,
    [leftAnimalBodies]: leftAnimalBodies + leftAnimalBodies + leftAnimalBodies + leftAnimalTails + enteringHole + bounce,
};
const validEnds = {
    [exitingHole + bounce]: leftAnimalTails + rightAnimalHeads + enteringHole,
    [rightAnimalHeads + leftAnimalTails + enteringHole]: singletons,
    [leftAnimalHeads]: leftAnimalTails + enteringHole,
    [rightAnimalTails]: rightAnimalHeads + enteringHole,
    [rightAnimalBodies]: rightAnimalHeads,
    [leftAnimalBodies]: leftAnimalTails,
};

function generateOriented(value){

    var newAnimal = '' + randomFrom(validStarts);
    for (var i = 0; i < value-1; i++) {
        last_char = newAnimal[i-1];
        for (const [predecessor, successor] of Object.entries(validSuccessors)) {
            if (predecessor.indexOf(last_char) > -1){
                newAnimal += randomFrom(successor);
                break;
            }
        }
    }
    last_char = newAnimal[i-1];
    for (const [predecessor, successor] of Object.entries(validEnds)) {
        if (predecessor.indexOf(last_char) > -1){
            newAnimal += randomFrom(successor);
            break;
        }
    }
    document.getElementById("oriented-generated-animal").innerHTML = makeBreakable(newAnimal);
}
generateOriented(document.getElementById("oriented-glyph-count").value);

</script>
{{< /raw >}}

```javascript
const rightAnimalHeads = "BEHKNRVZŻ";
const leftAnimalHeads = "yvspmieaź";
const rightAnimalTails = "ACFILOSWŹv";
const leftAnimalTails = "zxurolhdżE";
const rightAnimalBodies = "DGJMPQTUẊŽ";
const leftAnimalBodies = "wtqnkjgfḅž";
const singletons = ",*‐";
const exitingHole = "([{";
const enteringHole = ")]}";
const bounce = "«»$bcXY";

const validStarts = leftAnimalHeads + rightAnimalTails + exitingHole;
const validSuccessors = {
    [exitingHole + bounce]: rightAnimalHeads + rightAnimalBodies + leftAnimalBodies + leftAnimalTails + enteringHole + bounce,
    [enteringHole]: rightAnimalTails + leftAnimalHeads + exitingHole + singletons,
    [rightAnimalHeads + leftAnimalTails + singletons]: rightAnimalTails + leftAnimalHeads + exitingHole + singletons,
    [leftAnimalHeads]: leftAnimalBodies + leftAnimalBodies + leftAnimalBodies + leftAnimalTails + enteringHole + bounce,
    [rightAnimalTails]: rightAnimalBodies + rightAnimalBodies + rightAnimalBodies + rightAnimalHeads + enteringHole + bounce,
    [rightAnimalBodies]: rightAnimalBodies + rightAnimalBodies + rightAnimalBodies + rightAnimalHeads + enteringHole + bounce,
    [leftAnimalBodies]: leftAnimalBodies + leftAnimalBodies + leftAnimalBodies + leftAnimalTails + enteringHole + bounce,
};
const validEnds = {
    [exitingHole + bounce]: leftAnimalTails + rightAnimalHeads + enteringHole,
    [rightAnimalHeads + leftAnimalTails + enteringHole]: singletons,
    [leftAnimalHeads]: leftAnimalTails + enteringHole,
    [rightAnimalTails]: rightAnimalHeads + enteringHole,
    [rightAnimalBodies]: rightAnimalHeads,
    [leftAnimalBodies]: leftAnimalTails,
};

function generateOriented(value){

    var newAnimal = '' + randomFrom(validStarts);
    for (var i = 0; i < value-1; i++) {
        last_char = newAnimal[i-1];
        for (const [predecessor, successor] of Object.entries(validSuccessors)) {
            if (predecessor.indexOf(last_char) > -1){
                newAnimal += randomFrom(successor);
                break;
            }
        }
    }
    last_char = newAnimal[i-1];
    for (const [predecessor, successor] of Object.entries(validEnds)) {
        if (predecessor.indexOf(last_char) > -1){
            newAnimal += randomFrom(successor);
            break;
        }
    }
    return newAnimal;
}
```

## A regular grammar

Let's move up a level now.

What we've defined up to this point is a set of rules that, given a string, determine what characters are allowed next. This is called a [**formal grammar**](https://en.wikipedia.org/wiki/Formal_grammar) in Computer Science.

A grammar is defined primarily by:

- an **alphabet** of symbols (our Teranoptia font).
- a set of **starting characters**: all the characters that can be used at the start of the string (such as <span class="small teranoptia">a</span> or <span class="small teranoptia">*</span>).
- a set of **terminating character**: all the characters that can be used to terminate the string (such as <span class="small teranoptia">d</span> or <span class="small teranoptia">-</span>).
- a set of **production rules**: the rules needed to generate valid strings in that grammar. 

In our case, we're looking for a grammar that defines "well formed" animals. For example, our production rules might look like this:

- S (the start of the string) → a (<span class="small teranoptia">a</span>)
- a (<span class="small teranoptia">a</span>) → ad (<span class="small teranoptia">ad</span>)
- a (<span class="small teranoptia">a</span>) → ab (<span class="small teranoptia">ab</span>)
- b (<span class="small teranoptia">b</span>) → bb (<span class="small teranoptia">bb</span>)
- b (<span class="small teranoptia">b</span>) → bd (<span class="small teranoptia">bd</span>)
- d (<span class="small teranoptia">d</span>) → E (the end of the string)
- , (<span class="small teranoptia">,</span>) → E (the end of the string)

and so on. Each combination would have its own rule.

There are three main types of grammars according to Chomsky's hierarchy:

- **Regular grammars**: in all rules, the left-hand side is only a single nonterminal symbol and right-hand side may be the empty string, or a single terminal symbol, or a single terminal symbol followed by a nonterminal symbol, but nothing else. 
- **Context-free grammars**: in all rules, the left-hand side of each production rule consists of only a single nonterminal symbol, while the right-hand side may contain any number of terminal and non-terminal symbols.
- **Context-sensitive grammars**: rules can contain many terminal and non-terminal characters on both sides.

In our case, all the production rules look very much like the examples we defined above: one character on the left-hand side, at most two on the right-hand side. This means we're dealing with a regular grammar. And this is good news, because it means that this language can be encoded into a **regular expression**.

## Building the regex

Regular expressions are a very powerful tool, one that needs to be used with care. They're best used for string validation: given an arbitrary string, they are going to check whether it respects the grammar, i.e. whether the string it could have been generated by applying the rules above.

Having a regex for our Teranoptia animals will allow us to search for valid animals in long lists of stroings, for example an English dictionary. Such a search would have been prohibitively expensive without a regular expression: using one, while still quite costly, is orders of magnitude more efficient.

In order to build this complex regex, let's start with a very limited example: a regex that matches left-facing snakes.

```regex
^(a(b|c|X|Y)*d)+$
```

This regex is fairly straightforward: the string must start with a (<span class="small teranoptia">a</span>), can contain any number of b (<span class="small teranoptia">b</span>), c (<span class="small teranoptia">c</span>), X (<span class="small teranoptia">X</span>) and Y (<span class="small teranoptia">Y</span>), and must end with d (<span class="small teranoptia">d</span>). While we're at it, let's add a + to the end, meaning that this pattern can repeat multiple times: the string will simply contain many snakes.

### Left-facing snakes regex

{{< raw >}}
<div style="display: flex; gap: 10px;">
    <input id="left-facing-snakes-input" type="string" class="teranoptia" value="abd" oninput="validateLeftFacingSnake();"></input>
    <p id="left-facing-snakes-result">Valid</p>
</div>

<script>
var leftFacingSnake = new RegExp("^(a(b|c|X|Y)*d)+$");

function validateLeftFacingSnake(){
    const candidate = document.getElementById('left-facing-snakes-input').value;
    if (leftFacingSnake.test(candidate)){
        document.getElementById('left-facing-snakes-input').style.color = "green";
        document.getElementById('left-facing-snakes-result').innerHTML = "Valid!";
    } else {
        document.getElementById('left-facing-snakes-input').style.color = "red";
        document.getElementById('left-facing-snakes-result').innerHTML = "NOT valid!";
    }
}
validateLeftFacingSnake()
</script>
{{< /raw >}}

What would it take to extend it to snakes that face either side? Luckily, snake bodies are symmetrical, so we can take advantage of that and write:

```regex
^((a|W)(b|c|X|Y)*(d|Z))+$
```

### Naive snakes

{{< raw >}}
<div style="display: flex; gap: 10px;">
    <input id="naive-snakes-input" type="string" class="teranoptia" value="abdWXZ" oninput="validateNaiveSnake();"></input>
    <p id="naive-snakes-result">Valid</p>
</div>

<script>
var naiveSnake = new RegExp("^((a|W)(b|c|X|Y)*(d|Z))+$");

function validateNaiveSnake(){
    const candidate = document.getElementById('naive-snakes-input').value;
    if (naiveSnake.test(candidate)){
        document.getElementById('naive-snakes-input').style.color = "green";
        document.getElementById('naive-snakes-result').innerHTML = "Valid!";
    } else {
        document.getElementById('naive-snakes-input').style.color = "red";
        document.getElementById('naive-snakes-result').innerHTML = "NOT valid!";
    }
}
validateNaiveSnake();
</script>
{{< /raw >}}

That looks super-promising until we realize that there's a problem: this "snake" <span class="small teranoptia">aZ</span> also matches the regex. To generate well-formed animals we need to keep heads and tails separate. In the regex, it would look like:

```regex
^(
    (a)(b|c|X|Y)*(d) |
    (W)(b|c|X|Y)*(Z)
)+$
```

### Correct snakes

{{< raw >}}
<div style="display: flex; gap: 10px;">
    <input id="correct-snakes-input" type="string" class="teranoptia" value="abdWXZ" oninput="validateCorrectSnake();"></input>
    <p id="correct-snakes-result">Valid</p>
</div>

<script>
var correctSnake = new RegExp("^(((a)(b|c|X|Y)*(d))|((W)(b|c|X|Y)*(Z)))+$");

function validateCorrectSnake(){
    const candidate = document.getElementById('correct-snakes-input').value;
    if (correctSnake.test(candidate)){
        document.getElementById('correct-snakes-input').style.color = "green";
        document.getElementById('correct-snakes-result').innerHTML = "Valid!";
    } else {
        document.getElementById('correct-snakes-input').style.color = "red";
        document.getElementById('correct-snakes-result').innerHTML = "NOT valid!";
    }
}
validateCorrectSnake()
</script>
{{< /raw >}}

Once here, building the rest of the regex is simply matter of adding the correct characters to each group. We're gonna trade some extra characters for an easier structure by duplicating the symmetric characters when needed.

```regex
^(
    // Left-facing animals
    (
        y|v|s|p|m|i|e|a|ź|(|[|{   // Left heads & exiting holes
    )(
        w|t|q|n|k|j|g|f|ḅ|ž|X|Y|b|c|$|«|»  // Left & symmetric bodies
    )*(
        z|x|u|r|o|l|h|d|ż|E|)|]|}  // Left tails & entering holes
    ) |

    // Right facing animals
    (
        A|C|F|I|L|O|S|W|Ź|v|(|[|{   // right tails & exiting holes
    )(
        D|G|J|M|P|Q|T|U|Ẋ|Ž|b|c|X|Y|$|«|»  // right & symmetric bodies  
    )*(
        B|E|H|K|N|R|V|Z|Ż|)|]|}   // right heads & entering holes
    ) |

    // Singletons
    (,|-|*)
)+$
```

### Well-formed animals regex

{{< raw >}}
<div style="display: flex; gap: 10px;">
    <input id="correct-animal-input" type="string" class="teranoptia" value="abu*W«XZ" oninput="validateCorrectAnimal();"></input>
    <p id="correct-animal-result">Valid</p>
</div>

<script>
var correctAnimal = new RegExp("^((y|v|s|p|m|i|e|a|ź|\\(|\\[|\\{)(w|t|q|n|k|j|g|f|ḅ|ž|b|c|X|Y|\\$|«|»)*(z|x|u|r|o|l|h|d|ż|E|\\)|\\]|\\})|(A|C|F|I|L|O|S|W|Ź|v|\\(|\\[|\\{)(D|G|J|M|P|Q|T|U|Ẋ|Ž|b|c|X|Y|\\$|«|»)*(B|E|H|K|N|R|V|Z|Ż|\\)|\\]|\\})|(-|\\*|,))+$");

function validateCorrectAnimal(){
    const candidate = document.getElementById('correct-animal-input').value;
    if (correctAnimal.test(candidate)){
        document.getElementById('correct-animal-input').style.color = "green";
        document.getElementById('correct-animal-result').innerHTML = "Valid!";
    } else {
        document.getElementById('correct-animal-input').style.color = "red";
        document.getElementById('correct-animal-result').innerHTML = "NOT valid!";
    }
}
validateCorrectAnimal();
</script>
{{< /raw >}}

If you play with the above regex, you'll notice a slight discrepancy with what our well-formed animal generator creates. The generator can create "double-headed" monsters where a symmetric body part is inserted, like <span class="small teranoptia">a«Z</span>. However, the regex does not allow it. Extending it to account for these scenarios would make it even more unreadable, so this is left as an exercise for the reader.

## Searching for "monstrous" words

Let's put the regex to use! There must be some English words that match the regex, right?

Google helpfully compiled a text file with the most frequent 10.000 English words by frequency. Let's load it up and match every line with our brand-new regex. Unfortunately Teranoptia is case-sensitive and uses quite a few odd letters and special characters, so it's unlikely we're going to find many interesting creatures. Still worth an attempt.

### Monster search

{{< raw >}}
<div style="display: flex; gap: 10px;">
    <input id="file-url" type="url" value="https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt" style="width: 100%;"></input>
    <button onclick="searchFile();">Search</button>
</div>
<p id="search-result"></p>
<div id="words-found"></div>

<script>
var correctAnimal = new RegExp("^((y|v|s|p|m|i|e|a|ź|\\(|\\[|\\{)(w|t|q|n|k|j|g|f|ḅ|ž|b|c|X|Y|\\$|«|»)*(z|x|u|r|o|l|h|d|ż|E|\\)|\\]|\\})|(A|C|F|I|L|O|S|W|Ź|v|\\(|\\[|\\{)(D|G|J|M|P|Q|T|U|Ẋ|Ž|b|c|X|Y|\\$|«|»)*(B|E|H|K|N|R|V|Z|Ż|\\)|\\]|\\})|(-|\\*|,))+$");

function searchFile(){
    document.getElementById('search-result').innerHTML = "Loading...";

    fetch(document.getElementById('file-url').value)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        return response.text();
    })
    .then((text) => {
        lines = text.split('\n');
        counter = 0;

        for (i = 0; i < lines.length; i++){
            var candidate = lines[i];
            document.getElementById('search-result').innerHTML = "Checking " + candidate;
            if (correctAnimal.test(candidate)){
                document.getElementById('words-found').innerHTML += "<p>"+candidate+"<span class='teranoptia'> "+candidate+"</span></p>";
                counter++;
            }
        }
        document.getElementById('search-result').innerHTML = "Done! Found "+ counter +" animals over "+lines.length+" words tested.";        
    })
    .catch((error) => {
        document.getElementById('search-result').innerHTML = "Failed to fetch file :(";
    });
}
</script>
{{< /raw >}}

Go ahead and put your own vocabulary file to see if your language contains more animals!

## Conclusion

In this post I've just put together a few exercises for fun, but these tools can be great for teaching purposes: the output is very easy to validate visually, and the grammar involved, while not trivial, is not as complex as natural language or as dry as numerical sequences. If you need something to keep your students engaged, this might be a simple trick to help them visualize the concepts better.

On my side, I think I'm going to use these neat little monsters as weird [fleurons](https://en.wikipedia.org/wiki/Fleuron_(typography)) :)


<p class="fleuron"><a href="https://www.zansara.dev/posts/2024-05-06-teranoptia/">su</a></p>

---

_Download Teranoptia at this link: https://www.tunera.xyz/fonts/teranoptia/_






