// Preloaded data from the context
// Use variables defined in the HTML context
console.log(document.getElementById('fScoresData').textContent)
console.log(JSON.parse(document.getElementById('fScoresData').textContent))
let fScores = JSON.parse(document.getElementById('fScoresData').textContent);
let availableTags = JSON.parse(document.getElementById('availableTagsData').textContent);


function setAutoComplete(formId) {
    // Attach autocomplete to the first field in the form
    $(formId + " #name1").autocomplete({
        source: availableTags,
        focus: function (event, ui) {
            event.preventDefault();
            $(formId + " #name1").val(ui.item.label);
        },
        select: function (event, ui) {
            event.preventDefault();
            $(formId + " #name1").val(ui.item.label);
            $(formId + " #fangraphs_id1").val(ui.item.value);

            // Calculate fScore
            let weights = [5, 3, 1]; // Corresponding weights for the years 2024, 2025, and 2026
            let scores = [
                fScores[ui.item.value]?.[2024],
                fScores[ui.item.value]?.[2025],
                fScores[ui.item.value]?.[2026]
            ];

            // Calculate weighted score, ignoring missing values
            let totalWeight = 0;
            let weightedSum = 0;

            scores.forEach((score, index) => {
                if (score !== undefined) { // Only include if the score exists
                    weightedSum += score * weights[index];
                    totalWeight += weights[index];
                }
            });

            let score = totalWeight > 0 ? (weightedSum / totalWeight) : 0; // Avoid division by zero
            $(formId + " #fscore1").html(Math.round(score));


            // Add new input field dynamically
            addField(2, availableTags, formId);
        }
    });

    // Attach submit handler
    $(formId).on("submit", function (e) {
        e.preventDefault(); // Prevent normal form submission
        calculateTotalScore(formId);
    });
}

function addField(next, availableTags, formId) {
    // Create new field HTML
    let newField = `
        <div id="player${next}" class="player-row">
            <input type="hidden" name="fangraphs_id${next}" id="fangraphs_id${next}">
            <input type="text" name="name${next}" id="name${next}" class="player-name">
            <label class="fscore_label" id="fscore${next}"></label>
            <button type="button" class="delete-button" onclick="deleteField(${next}, '${formId}')" style="background: none; border: none; cursor: pointer;">
                <i class="fas fa-trash-alt"></i>
            </button>
        </div>`;
    $(formId + " #player" + (next - 1)).after(newField);

    // Attach autocomplete to the new field
    $(formId + " #name" + next).autocomplete({
        source: availableTags,
        focus: function (event, ui) {
            event.preventDefault();
            $(formId + " #name" + next).val(ui.item.label);
        },
        select: function (event, ui) {
            event.preventDefault();
            $(formId + " #name" + next).val(ui.item.label);
            $(formId + " #fangraphs_id" + next).val(ui.item.value);

            // Calculate fScore
            let weights = [5, 3, 1]; // Corresponding weights for the years 2024, 2025, and 2026
            let scores = [
                fScores[ui.item.value]?.[2024],
                fScores[ui.item.value]?.[2025],
                fScores[ui.item.value]?.[2026]
            ];

            // Calculate weighted score, ignoring missing values
            let totalWeight = 0;
            let weightedSum = 0;

            scores.forEach((score, index) => {
                if (score !== undefined) { // Only include if the score exists
                    weightedSum += score * weights[index];
                    totalWeight += weights[index];
                }
            });

            // Calculate the final score for this field
            let score = totalWeight > 0 ? (weightedSum / totalWeight) : 0; // Avoid division by zero
            $(formId + " #fscore" + next).html(Math.round(score));

            // Add the next field dynamically
            addField(next + 1, availableTags, formId);
        }
    });
}



function deleteField(id, formId) {
    $(formId + " #player" + id).remove();
}

function calculateTotalScore(formId) {
    let total = 0;
    $(formId + " .fscore_label").each(function () {
        let score = parseInt($(this).text());
        if (!isNaN(score)) {
            total += score;
        }
    });
    $(formId + " .total_score").html(total);
}

$(document).ready(function () {
    setAutoComplete("#trade_form1");
    setAutoComplete("#trade_form2");
});