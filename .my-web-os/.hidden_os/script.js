async function handleEnter(e) {
    if (e.key === 'Enter') {
        const cmd = document.getElementById('prompt').value;
        const res = await fetch('/execute', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({cmd})
        });
        const data = await res.json();
        document.getElementById('output').innerText += "\n> " + cmd + "\n" + data.output;
    }
}
