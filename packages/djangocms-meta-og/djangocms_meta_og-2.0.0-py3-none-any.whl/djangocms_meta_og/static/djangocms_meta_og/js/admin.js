function addValueIntoField(meta, node, fncInsertText) {
    node.style.cursor = "pointer";
    node.title = gettext("Add this value to the META field.")
    node.addEventListener("click", function (event) {
        fncInsertText(meta, event.target.textContent)
    })
}

document.addEventListener('DOMContentLoaded', function () {
    const meta = document.querySelector('textarea[name=meta]')
    if (meta) {
        for (const node of document.querySelectorAll('.meta-og-help ul.meta-og-property li')) {
            addValueIntoField(meta, node, function (textarea, text) {
                textarea.value += "\n" + text + " "
            })
        }
        for (const node of document.querySelectorAll('.meta-og-help ul.meta-og-content li')) {
            addValueIntoField(meta, node, function (textarea, text) {
                textarea.value += "\n" + text + "\n"
            })
        }
        for (const node of document.querySelectorAll('.meta-og-help ul.meta-og-dynamic-content li code strong')) {
            addValueIntoField(meta, node, function (textarea, text) {
                textarea.value += " " + text + "\n"
            })
        }
    }
})
