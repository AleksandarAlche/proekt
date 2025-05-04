let mvpData = null;
let dpoyData = null;
let currentViewMode = "mvp";

document.addEventListener("DOMContentLoaded", function () {
  Promise.all([
    fetch("mvp_predictions_data.json").then((response) => {
      if (!response.ok) throw new Error("Error loading MVP data");
      return response.json();
    }),
    fetch("dpoy_predictions_data.json").then((response) => {
      if (!response.ok) throw new Error("Error loading DPOY data");
      return response.json();
    }),
  ])
    .then(([mvpDataResponse, dpoyDataResponse]) => {
      mvpData = mvpDataResponse;
      dpoyData = dpoyDataResponse;

      updateUI(mvpData);
      setupEventListeners();
    })
    .catch((error) => {
      console.error("Error loading prediction data:", error);
      document.getElementById("predictionsBody").innerHTML = `
      <tr>
        <td colspan="4" class="loading">
          Error loading data. Please make sure you've run the Python export script first.
        </td>
      </tr>
    `;
    });

  document.getElementById("mvpToggle").addEventListener("click", function () {
    if (currentViewMode !== "mvp") {
      currentViewMode = "mvp";
      updateUI(mvpData);
      updateActiveToggle();
    }
  });

  document.getElementById("dpoyToggle").addEventListener("click", function () {
    if (currentViewMode !== "dpoy") {
      currentViewMode = "dpoy";
      updateUI(dpoyData);
      updateActiveToggle();
    }
  });
});

function updateActiveToggle() {
  document
    .getElementById("mvpToggle")
    .classList.toggle("active", currentViewMode === "mvp");
  document
    .getElementById("dpoyToggle")
    .classList.toggle("active", currentViewMode === "dpoy");

  const tableHeader = document.getElementById("predictionsHeader");

  if (currentViewMode === "mvp") {
    tableHeader.innerHTML = `
      <th>Season</th>
      <th>Should Be MVP</th>
      <th>Actual MVP</th>
      <th>Match</th>
    `;
  } else {
    tableHeader.innerHTML = `
      <th>Season</th>
      <th>Should Be DPOY</th>
      <th>Actual DPOY</th>
      <th>Match</th>
    `;
  }
}

function updateUI(data) {
  document.getElementById("accuracyText").textContent = `${(
    data.accuracy * 100
  ).toFixed(0)}%`;
  document.getElementById("totalSeasons").textContent = data.totalSeasons;
  document.getElementById("correctPredictions").textContent =
    data.correctPredictions;

  createAccuracyChart(data.accuracy);
  populateTable(data.predictions);
  updateFeatureList(data.features);
}

function createAccuracyChart(accuracy) {
  const ctx = document.getElementById("accuracyChart").getContext("2d");

  if (window.accuracyChartInstance) {
    window.accuracyChartInstance.destroy();
  }

  window.accuracyChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      datasets: [
        {
          data: [accuracy * 100, (1 - accuracy) * 100],
          backgroundColor: ["#17408B", "#f2f2f2"],
          borderWidth: 0,
        },
      ],
    },
    options: {
      cutout: "70%",
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          enabled: false,
        },
      },
    },
  });
}

function updateFeatureList(features) {
  const featureList = document.getElementById("featureList");
  featureList.innerHTML = "";

  features.forEach((feature) => {
    const featureTag = document.createElement("div");
    featureTag.className = "feature-tag";
    featureTag.textContent = feature;
    featureList.appendChild(featureTag);
  });
}

function populateTable(predictions) {
  const tableBody = document.getElementById("predictionsBody");
  tableBody.innerHTML = "";

  predictions.forEach((prediction) => {
    const row = document.createElement("tr");

    if (currentViewMode === "mvp") {
      row.dataset.predicted = prediction.shouldBeMvp.toLowerCase();
      row.dataset.actual = prediction.actualMvp.toLowerCase();
      row.innerHTML = `
        <td>${prediction.season}-${(prediction.season + 1)
        .toString()
        .slice(2)}</td>
        <td>${prediction.shouldBeMvp}</td>
        <td>${prediction.actualMvp}</td>
        <td class="${prediction.match ? "match" : "no-match"}">${
        prediction.match ? "✓" : "✗"
      }</td>
      `;
    } else {
      row.dataset.predicted = prediction.shouldBeDpoy.toLowerCase();
      row.dataset.actual = prediction.actualDpoy.toLowerCase();
      row.innerHTML = `
        <td>${prediction.season}-${(prediction.season + 1)
        .toString()
        .slice(2)}</td>
        <td>${prediction.shouldBeDpoy}</td>
        <td>${prediction.actualDpoy}</td>
        <td class="${prediction.match ? "match" : "no-match"}">${
        prediction.match ? "✓" : "✗"
      }</td>
      `;
    }

    row.dataset.filter = prediction.match ? "match" : "no-match";
    tableBody.appendChild(row);
  });
}

function setupEventListeners() {
  const searchInput = document.getElementById("search");
  searchInput.addEventListener("input", function () {
    const searchTerm = this.value.toLowerCase();
    const rows = document.querySelectorAll("#predictionsBody tr");

    rows.forEach((row) => {
      const predicted = row.dataset.predicted;
      const actual = row.dataset.actual;
      const currentFilter =
        document.querySelector(".filter-btn.active").dataset.filter;
      const matchesSearch =
        predicted.includes(searchTerm) || actual.includes(searchTerm);
      const matchesFilter =
        currentFilter === "all" || row.dataset.filter === currentFilter;

      row.style.display = matchesSearch && matchesFilter ? "" : "none";
    });
  });

  const filterButtons = document.querySelectorAll(".filter-btn");
  filterButtons.forEach((button) => {
    button.addEventListener("click", function () {
      document.querySelector(".filter-btn.active").classList.remove("active");
      this.classList.add("active");

      const filterValue = this.dataset.filter;
      const searchTerm = document.getElementById("search").value.toLowerCase();
      const rows = document.querySelectorAll("#predictionsBody tr");

      rows.forEach((row) => {
        const predicted = row.dataset.predicted;
        const actual = row.dataset.actual;
        const matchesSearch =
          predicted.includes(searchTerm) || actual.includes(searchTerm);
        const matchesFilter =
          filterValue === "all" || row.dataset.filter === filterValue;

        row.style.display = matchesSearch && matchesFilter ? "" : "none";
      });
    });
  });
}
