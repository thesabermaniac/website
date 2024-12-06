// Preloaded data from the context
const fScores = JSON.parse(document.getElementById('fScoresData').textContent);
const availableTags = JSON.parse(document.getElementById('availableTagsData').textContent);

// Common function to calculate fScore
function calculateScore(playerValue) {
    const weights = [5, 3, 1];
    const rebuildingWeights = [1, 3, 5];
    const scores = [2024, 2025, 2026].map(year => fScores[playerValue]?.[year]);

    let totalWeight = 0, weightedSum = 0, totalRebuildingWeight = 0, rebuildingWeightedSum = 0;

    scores.forEach((score, index) => {
        if (score !== undefined) {
            weightedSum += score * weights[index];
            totalWeight += weights[index];
            rebuildingWeightedSum += score * rebuildingWeights[index];
            totalRebuildingWeight += rebuildingWeights[index];
        }
    });

    return {
        score: totalWeight ? Math.round(weightedSum / totalWeight) : 0,
        rebuildingScore: totalRebuildingWeight ? Math.round(rebuildingWeightedSum / totalRebuildingWeight) : 0
    };
}

// Function to initialize autocomplete and calculate scores
function initializeAutocomplete(inputId, formId, next) {
    $(inputId).autocomplete({
        source: availableTags,
        focus: function (event, ui) {
            event.preventDefault();
            $(inputId).val(ui.item.label);
        },
        select: function (event, ui) {
            event.preventDefault();
            $(inputId).val(ui.item.label);
            $(`${formId} #fangraphs_id${next}`).val(ui.item.value);

            // Calculate and display the scores
            const { score, rebuildingScore } = calculateScore(ui.item.value);
            $(`${formId} #fscore${next}`).text(score);
            $(`${formId} #rebuilding_score${next}`).text(rebuildingScore);

            // Add next field dynamically
            addField(next + 1, formId);
        }
    });
}

// Set autocomplete for the form
function setAutoComplete(formId) {
    initializeAutocomplete(`${formId} #name1`, formId, 1);

    // Handle the clear button for this form
    $(`${formId} #clearButton`).on('click', function () {
        const form = $(this).closest('form');
        form.find(".player-name").val(""); // Clear player input fields
        form.find(".fscore_label, .rebuilding_fscore_label").text(""); // Clear scores
        form.find(".player-row").not(':first').remove(); // Remove extra rows
        setAutoComplete(formId); // Reinitialize autocomplete
    });
}

// Add new field dynamically
function addField(next, formId) {
    const newField = `
        <div id="player${next}" class="player-row">
            <div class="table-cell">
                <input type="hidden" name="fangraphs_id${next}" id="fangraphs_id${next}">
                <input type="text" name="name${next}" id="name${next}" class="player-name">
            </div>
            <div class="table-cell">
                <label class="fscore_label" id="fscore${next}"></label>
            </div>
            <div class="table-cell">
                <label class="rebuilding_fscore_label" id="rebuilding_score${next}"></label>
            </div>
            <button type="button" class="delete-button" onclick="deleteField(${next}, '${formId}')">
                <i class="fas fa-trash-alt"></i>
            </button>
        </div>`;

    $(`${formId} #player${next - 1}`).after(newField);
    initializeAutocomplete(`${formId} #name${next}`, formId, next);
}

// Delete player field dynamically
function deleteField(id, formId) {
    $(`${formId} #player${id}`).remove();
}

// Calculate total scores for a form
function calculateTotalScores(formId) {
    let winNowTotal = 0, rebuildingTotal = 0;

    $(`${formId} .fscore_label`).each(function () {
        const score = parseInt($(this).text());
        if (!isNaN(score)) winNowTotal += score;
    });

    $(`${formId} .rebuilding_fscore_label`).each(function () {
        const rebuildingScore = parseInt($(this).text());
        if (!isNaN(rebuildingScore)) rebuildingTotal += rebuildingScore;
    });

    return { winNowTotal, rebuildingTotal };
}

// Generate comparison table
function generateComparisonTable(results) {
    const tableBody = $("#comparisonTable tbody").empty(); // Clear existing rows

    results.forEach(result => {
        const row = `<tr>
                        <td>${result.teamName}</td>
                        <td>${result.winNowTotal}</td>
                        <td>${result.rebuildingTotal}</td>
                    </tr>`;
        tableBody.append(row);
    });

    $(".results-container").show();
}

// Submit button handler
$("#submitButton").on("click", function () {
    const results = $(".trade-form").map(function () {
        const formId = "#" + $(this).attr("id");
        const teamName = $(formId).find(".team-title").text();
        const { winNowTotal, rebuildingTotal } = calculateTotalScores(formId);

        return { teamName, winNowTotal, rebuildingTotal };
    }).get();

    generateComparisonTable(results);
});

$(document).ready(function () {
    // Initialize autocomplete for the forms
    setAutoComplete("#trade_form1");
    setAutoComplete("#trade_form2");
});
