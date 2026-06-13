let overview = null;
let activeValidationJob = null;
let activeScrapJob = null;

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Request failed");
  }
  return data;
}

function switchPanel(panelId) {
  $$(".tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.panel === panelId));
  $$(".panel").forEach((panel) => panel.classList.toggle("active", panel.id === panelId));
}

function renderMetrics(metrics) {
  const strip = $("#metricsStrip");
  strip.innerHTML = "";
  if (!metrics.length) {
    strip.innerHTML = '<div class="metric-card"><span>Status</span><strong>No metrics yet</strong></div>';
    return;
  }
  metrics.forEach((metric) => {
    const card = document.createElement("article");
    card.className = "metric-card";
    card.innerHTML = `<span>${metric.Metric}</span><strong>${metric.Value}</strong>`;
    strip.appendChild(card);
  });
}

function renderRunSummary(summary) {
  const box = $("#runSummary");
  if (!summary || !summary.city) {
    box.textContent = "No forecast run summary found yet.";
    return;
  }
  box.innerHTML = `
    <strong>${summary.city}</strong>
    <span>Data: ${summary.data_start_date} to ${summary.data_end_date}</span>
    <span>Forecast: ${summary.forecast_start_date} to ${summary.forecast_end_date} (${summary.forecast_days} days)</span>
    <span>Train: ${summary.train_start_date} to ${summary.train_end_date}</span>
  `;
}

function renderValidationSummary(summary, metrics) {
  const box = $("#validationSummary");
  if (!summary || !summary.city) {
    box.innerHTML = '<article class="metric-card"><span>Status</span><strong>No validation run yet</strong></article>';
    return;
  }
  const metricCards = (metrics || [])
    .map((metric) => `<article class="metric-card"><span>${metric.Metric}</span><strong>${metric.Value}</strong></article>`)
    .join("");
  box.innerHTML = `
    <article class="metric-card wide">
      <span>City</span>
      <strong>${summary.city}</strong>
      <p>Train before ${summary.forecast_start_date}. Recursive test from ${summary.test_start_date} to ${summary.test_end_date}.</p>
    </article>
    ${metricCards}
  `;
}

function renderScrapConfig(config) {
  if (!config) return;
  $("#scrapStartDate").value = config.startDate || "";
  $("#scrapEndDate").value = config.endDate || "";
  $("#scrapYearsBack").value = config.yearsBack || "10";
  $("#scrapHeadless").value = config.headless || "False";
  $("#scrapMaxWaitTime").value = config.maxWaitTime || "15";
  $("#scrapSaveFormats").value = config.saveFormats || "csv";
  $("#scrapOverwrite").value = config.overwrite || "False";
  $("#scrapWebsiteDelay").value = config.websiteDelay || "1.0";
  $("#scrapWeatherDelay").value = config.weatherDelay || "2.0";
}

function renderCities(cities) {
  const select = $("#city");
  select.innerHTML = "";
  cities.forEach((city) => {
    const option = document.createElement("option");
    option.value = city;
    option.textContent = city;
    option.selected = city === "Barwala";
    select.appendChild(option);
  });
}

function renderFlow(steps) {
  const grid = $("#scrapFlow");
  grid.innerHTML = "";
  steps.forEach((step, index) => {
    const card = document.createElement("article");
    card.className = "flow-card";
    card.innerHTML = `<span>${index + 1}</span><p>${step}</p>`;
    grid.appendChild(card);
  });
}

function renderCharts(charts) {
  const grid = $("#chartGrid");
  grid.innerHTML = "";
  charts.forEach((chart) => {
    const card = document.createElement("article");
    card.className = "chart-card";
    const statusClass = chart.exists ? "" : "missing";
    const statusText = chart.exists ? "Available" : "Missing";
    card.innerHTML = `
      <header>
        <strong>${chart.title}</strong>
        <span class="status-pill ${statusClass}">${statusText}</span>
      </header>
      ${
        chart.exists
          ? `<iframe src="${chart.url}" title="${chart.title}" loading="lazy"></iframe>`
          : `<div class="missing-chart">Run validation to create this chart.</div>`
      }
    `;
    grid.appendChild(card);
  });
}

function renderDatasets(datasets) {
  const grid = $("#datasetGrid");
  grid.innerHTML = "";
  datasets.forEach((dataset) => {
    const card = document.createElement("article");
    card.className = "dataset-card";
    const statusClass = dataset.exists ? "" : "missing";
    const statusText = dataset.exists ? `${dataset.row_count} rows` : "Missing";

    let table = "<p class='hint'>File not found yet.</p>";
    if (dataset.exists && dataset.rows.length) {
      const columns = dataset.columns.slice(0, 10);
      const head = columns.map((column) => `<th>${column}</th>`).join("");
      const rows = dataset.rows
        .map((row) => `<tr>${columns.map((column) => `<td>${row[column] ?? ""}</td>`).join("")}</tr>`)
        .join("");
      table = `<div class="table-wrap"><table><thead><tr>${head}</tr></thead><tbody>${rows}</tbody></table></div>`;
    }

    card.innerHTML = `
      <header>
        <div>
          <strong>${dataset.name}</strong>
          <div class="hint">${dataset.path}</div>
        </div>
        <span class="status-pill ${statusClass}">${statusText}</span>
      </header>
      ${table}
    `;
    grid.appendChild(card);
  });
}

async function refreshOverview() {
  overview = await api("/api/overview");
  $("#username").textContent = overview.username;
  renderMetrics(overview.metrics);
  renderRunSummary(overview.runSummary);
  renderValidationSummary(overview.runSummary, overview.metrics);
  renderScrapConfig(overview.scrapConfig);
  renderCities(overview.cities);
  renderFlow(overview.scrapFlow);
  renderCharts(overview.charts);
  renderDatasets(overview.datasets);
}

function formatJob(job) {
  const returnCodeText = job.status === "stopped" ? "stopped by user" : (job.returncode ?? "running");
  const header = [
    `Job: ${job.kind}`,
    `Status: ${job.status}`,
    `Return code: ${returnCodeText}`,
    "",
  ];
  return header.concat(job.log || []).join("\n");
}

async function watchJob(jobId, logElement, onDone, stopButton) {
  let job;
  try {
    job = await api(`/api/jobs/${jobId}`);
  } catch (error) {
    logElement.textContent += `\nUnable to refresh job status: ${error.message}`;
    if (stopButton) {
      stopButton.style.display = "none";
      stopButton.disabled = false;
      stopButton.textContent = stopButton.dataset.idleText || "Stop";
    }
    if (onDone) onDone({ status: "failed", error });
    return;
  }

  logElement.textContent = formatJob(job);
  logElement.scrollTop = logElement.scrollHeight;

  if (job.status === "running" || job.status === "queued") {
    if (stopButton) {
      stopButton.style.display = "inline-block";
      stopButton.disabled = false;
    }
    setTimeout(() => watchJob(jobId, logElement, onDone, stopButton), 1000);
    return;
  }
  
  // Job has finished (completed, failed, or stopped)
  if (stopButton) {
    stopButton.style.display = "none";
    stopButton.disabled = false;
    stopButton.textContent = stopButton.dataset.idleText || "Stop";
  }
  if (onDone) onDone(job);
  refreshOverview().catch((error) => {
    logElement.textContent += `\nUnable to refresh overview: ${error.message}`;
  });
}

function setButtonLoading(button, isLoading, label) {
  button.disabled = isLoading;
  if (isLoading) {
    button.innerHTML = `<span class="spinner"></span>${label}`;
    return;
  }
  button.textContent = button.dataset.idleText || label;
}

async function stopJob(jobId, stopButton, onStopped) {
  console.log("Stop button clicked for job:", jobId);
  if (stopButton) {
    stopButton.disabled = true;
    stopButton.textContent = "Stopping...";
  }
  try {
    const response = await api(`/api/jobs/${jobId}/stop`, {
      method: "POST",
      body: JSON.stringify({}),
    });
    console.log("Stop response:", response);
    if (stopButton) {
      stopButton.textContent = "Stopped";
    }
    if (onStopped) onStopped(response);
    // Refresh job status immediately
    setTimeout(() => {
      if (stopButton) {
        stopButton.style.display = "none";
        stopButton.disabled = false;
        stopButton.textContent = stopButton.dataset.idleText || "Stop";
      }
    }, 500);
  } catch (error) {
    console.error("Error stopping job:", error);
    if (stopButton) {
      stopButton.disabled = false;
      stopButton.textContent = "Stop Failed";
    }
    alert("Error stopping job: " + error.message);
  }
}

async function runValidation(event) {
  event.preventDefault();
  const payload = {
    city: $("#city").value,
  };
  const log = $("#validationLog");
  const button = $("#runValidation");
  const stopButton = $("#stopValidation");
  setButtonLoading(button, true, "Running Validation");
  log.textContent = "Starting validation job...";
  try {
    const job = await api("/api/validation/run", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    activeValidationJob = job.id;
    stopButton.dataset.idleText = "Stop Validation";
    stopButton.onclick = () => stopJob(
      activeValidationJob,
      stopButton,
      () => setButtonLoading(button, false, "Run Validation")
    );
    watchJob(activeValidationJob, log, () => setButtonLoading(button, false, "Run Validation"), stopButton);
  } catch (error) {
    log.textContent = error.message;
    setButtonLoading(button, false, "Run Validation");
  }
}

async function runScrap() {
  const payload = {
    startDate: $("#scrapStartDate").value,
    endDate: $("#scrapEndDate").value,
    yearsBack: $("#scrapYearsBack").value,
    headless: $("#scrapHeadless").value,
    maxWaitTime: $("#scrapMaxWaitTime").value,
    saveFormats: $("#scrapSaveFormats").value,
    overwrite: $("#scrapOverwrite").value,
    websiteDelay: $("#scrapWebsiteDelay").value,
    weatherDelay: $("#scrapWeatherDelay").value,
  };
  const log = $("#scrapLog");
  const button = $("#runScrap");
  const stopButton = $("#stopScrap");
  setButtonLoading(button, true, "Running Data Scrap");
  log.textContent = "Starting data scrap pipeline...";
  try {
    const job = await api("/api/data-scrap/run", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    activeScrapJob = job.id;
    stopButton.dataset.idleText = "Stop Data Scrap";
    stopButton.onclick = () => stopJob(
      activeScrapJob,
      stopButton,
      () => setButtonLoading(button, false, "Run Data Scrap Pipeline")
    );
    watchJob(activeScrapJob, log, () => setButtonLoading(button, false, "Run Data Scrap Pipeline"), stopButton);
  } catch (error) {
    log.textContent = error.message;
    setButtonLoading(button, false, "Run Data Scrap Pipeline");
  }
}

function bindEvents() {
  $$(".tab").forEach((tab) => tab.addEventListener("click", () => switchPanel(tab.dataset.panel)));
  $("#showScrap").addEventListener("click", () => switchPanel("scrapPanel"));
  $("#showValidation").addEventListener("click", () => switchPanel("validationPanel"));
  $("#validationForm").addEventListener("submit", runValidation);
  $("#scrapForm").addEventListener("submit", (event) => {
    event.preventDefault();
    runScrap();
  });
}

bindEvents();
refreshOverview().catch((error) => {
  document.body.innerHTML = `<main><pre class="log-box">Application failed to load: ${error.message}</pre></main>`;
});
