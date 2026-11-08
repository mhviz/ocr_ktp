const $ = (id) => document.getElementById(id);
const fields = [
  ["provinsi", "Provinsi"], ["kabupaten_kota", "Kabupaten / Kota"], ["nik", "NIK"], ["nama", "Nama"],
  ["tempat_tgl_lahir", "Tempat / Tanggal Lahir"], ["jenis_kelamin", "Jenis Kelamin"], ["golongan_darah", "Golongan Darah"], ["alamat", "Alamat"],
  ["rt_rw", "RT / RW"], ["kel_desa", "Kelurahan / Desa"], ["kecamatan", "Kecamatan"], ["agama", "Agama"],
  ["status_perkawinan", "Status Perkawinan"], ["pekerjaan", "Pekerjaan"], ["kewarganegaraan", "Kewarganegaraan"], ["berlaku_hingga", "Berlaku Hingga"],
];
let config = { providers: [] };
let selectedProvider = "apple";
let selectedFile = null;
let currentResult = null;
let elapsedInterval = null;
let previewObjectUrl = null;

$("year").textContent = new Date().getFullYear();

function formatDuration(ms) {
  if (ms < 1000) return `${Math.round(ms)} ms`;
  return `${(ms / 1000).toFixed(2)} s`;
}

function updateSummary(providerId, modelName, state) {
  const providerMap = { apple: "Apple Foundation Models", openai: "OpenAI-Compatible API" };
  $("summary-provider").textContent = providerMap[providerId] || providerId;
  $("summary-model").textContent = modelName || "—";
  $("summary-state").textContent = state || "Ready";
}

function renderProviders() {
  const list = $("provider-list");
  list.replaceChildren();
  for (const provider of config.providers) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `provider-card${selectedProvider === provider.id ? " selected" : ""}`;
    button.dataset.provider = provider.id;
    button.disabled = !provider.available;
    const icon = document.createElement("span");
    icon.className = "provider-icon";
    icon.textContent = provider.id === "apple" ? "◒" : "✦";
    const copy = document.createElement("span");
    copy.className = "provider-copy";
    const title = document.createElement("span");
    title.className = "provider-title";
    title.textContent = provider.name;
    const model = document.createElement("span");
    model.className = "provider-model";
    model.textContent = provider.model;
    const desc = document.createElement("span");
    desc.className = "provider-desc";
    desc.textContent = provider.available
      ? `${provider.mode} · ${provider.description}`
      : `${provider.mode}. This provider is unavailable on this machine.`;
    copy.append(title, model, desc);
    const radio = document.createElement("span");
    radio.className = "radio-mark";
    button.append(icon, copy, radio);
    button.addEventListener("click", () => {
      if (!provider.available) return;
      selectedProvider = provider.id;
      renderProviders();
      updateSummary(selectedProvider, provider.model, "Ready");
    });
    list.append(button);
  }
  const activeProvider = config.providers.find((provider) => provider.id === selectedProvider) || config.providers[0];
  if (activeProvider) {
    updateSummary(activeProvider.id, activeProvider.model, activeProvider.available ? "Ready" : "Unavailable");
  }
}

async function loadConfig() {
  try {
    const response = await fetch("/api/config");
    if (!response.ok) throw new Error("Could not load provider configuration.");
    config = await response.json();
    if (!config.providers.length) {
      $("provider-list").textContent = "No providers are configured yet.";
      return;
    }
    if (!config.providers.some((p) => p.id === selectedProvider && p.available)) {
      selectedProvider = config.providers.find((p) => p.available)?.id || config.providers[0].id;
    }
    renderProviders();
  } catch (error) {
    $("provider-list").textContent = error.message;
  }
}

function showFile(file) {
  clearError();
  if (!/\.(jpe?g|png|pdf)$/i.test(file.name)) return showFileError("Choose a JPG, PNG, or PDF file.");
  if (file.size > 10 * 1024 * 1024) return showFileError("File size must be below 10 MB.");
  selectedFile = file;
  $("file-name").textContent = file.name;
  $("file-size").textContent = `${(file.size / 1024).toFixed(1)} KB · ${file.type || "document"}`;
  $("file-card").classList.remove("hidden");
  $("extract-button").disabled = false;
  $("preview-empty").classList.add("hidden");
  $("preview-image-wrap").classList.remove("hidden");
  const isImage = file.type.startsWith("image/") || /\.(jpe?g|png)$/i.test(file.name);
  $("preview-image").classList.toggle("hidden", !isImage);
  $("pdf-preview-label").classList.toggle("hidden", isImage);
  if (previewObjectUrl) URL.revokeObjectURL(previewObjectUrl);
  if (isImage) {
    previewObjectUrl = URL.createObjectURL(file);
    $("preview-image").src = previewObjectUrl;
  }
  $("results-section").classList.add("hidden");
  $("error-panel").classList.add("hidden");
}

function showFileError(message) {
  $("file-error").textContent = message;
  $("file-error").classList.remove("hidden");
}
function clearError() { $("file-error").classList.add("hidden"); }
function removeFile() {
  selectedFile = null;
  $("file-input").value = "";
  $("file-card").classList.add("hidden");
  $("extract-button").disabled = true;
  $("preview-empty").classList.remove("hidden");
  $("preview-image-wrap").classList.add("hidden");
  $("preview-image").src = "";
  if (previewObjectUrl) URL.revokeObjectURL(previewObjectUrl);
  previewObjectUrl = null;
  $("results-section").classList.add("hidden");
  clearError();
}

$("browse-button").addEventListener("click", () => $("file-input").click());
$("dropzone").addEventListener("click", (event) => {
  if (event.target !== $("browse-button")) $("file-input").click();
});
$("dropzone").addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    $("file-input").click();
  }
});
$("file-input").addEventListener("change", (event) => {
  if (event.target.files[0]) showFile(event.target.files[0]);
});
$("remove-file").addEventListener("click", removeFile);
for (const eventName of ["dragenter", "dragover"]) {
  $("dropzone").addEventListener(eventName, (event) => {
    event.preventDefault();
    $("dropzone").classList.add("drag-over");
  });
}
for (const eventName of ["dragleave", "drop"]) {
  $("dropzone").addEventListener(eventName, (event) => {
    event.preventDefault();
    $("dropzone").classList.remove("drag-over");
  });
}
$("dropzone").addEventListener("drop", (event) => {
  if (event.dataTransfer.files[0]) showFile(event.dataTransfer.files[0]);
});

function setProcessing(active) {
  $("extract-button").disabled = active || !selectedFile;
  $("progress-panel").classList.toggle("hidden", !active);
  if (active) {
    const start = performance.now();
    $("elapsed-live").textContent = "0.0 s";
    elapsedInterval = setInterval(() => {
      $("elapsed-live").textContent = `${((performance.now() - start) / 1000).toFixed(1)} s`;
    }, 100);
    updateSummary(selectedProvider, $("summary-model").textContent, "Processing");
  } else if (elapsedInterval) {
    clearInterval(elapsedInterval);
    elapsedInterval = null;
  }
}

function showError(message) {
  $("error-message").textContent = message;
  $("error-panel").classList.remove("hidden");
}

function renderResults(result, model, serverTime, totalTime) {
  currentResult = result;
  $("total-time").textContent = formatDuration(totalTime);
  $("server-time").textContent = formatDuration(serverTime);
  $("result-model").textContent = model;
  $("fields-count").textContent = `${Object.values(result).filter(Boolean).length} / ${fields.length}`;
  const grid = $("fields-grid");
  grid.replaceChildren();
  for (const [key, label] of fields) {
    const item = document.createElement("div");
    item.className = "field-item";
    const caption = document.createElement("label");
    caption.htmlFor = `field-${key}`;
    caption.textContent = label;
    const input = document.createElement("input");
    input.id = `field-${key}`;
    input.value = result[key] || "";
    input.autocomplete = "off";
    input.addEventListener("input", () => { currentResult[key] = input.value; });
    item.append(caption, input);
    grid.append(item);
  }
  $("copy-status").classList.add("hidden");
  $("results-section").classList.remove("hidden");
  updateSummary(selectedProvider, model, "Complete");
  $("results-section").scrollIntoView({ behavior: "smooth", block: "start" });
}

$("extract-button").addEventListener("click", async () => {
  if (!selectedFile) return;
  $("error-panel").classList.add("hidden");
  $("results-section").classList.add("hidden");
  $("progress-title").textContent = "Working on your document…";
  $("progress-subtitle").textContent = "Securely processing with your selected model.";
  setProcessing(true);
  const started = performance.now();
  try {
    const form = new FormData();
    form.append("provider", selectedProvider);
    form.append("file", selectedFile);
    const response = await fetch("/api/extract", { method: "POST", body: form });
    const totalTime = performance.now() - started;
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.detail || "Processing failed.");
    setProcessing(false);
    renderResults(payload.result, payload.model, payload.processing_time_ms, totalTime);
  } catch (error) {
    setProcessing(false);
    showError(error.message || "The application server could not complete the request.");
    updateSummary(selectedProvider, $("summary-model").textContent, "Error");
  }
});

async function copyJson() {
  if (!currentResult) return;
  const json = JSON.stringify(currentResult, null, 2);
  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(json);
    } else {
      const textarea = document.createElement("textarea");
      textarea.value = json;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.append(textarea);
      textarea.select();
      const copied = document.execCommand("copy");
      textarea.remove();
      if (!copied) throw new Error("Clipboard access was denied.");
    }
    $("copy-status").textContent = "JSON copied to clipboard.";
    $("copy-status").classList.remove("hidden");
  } catch {
    $("copy-status").textContent = "Could not copy automatically. Please use Download JSON instead.";
    $("copy-status").classList.remove("hidden");
  }
}

$("copy-json-button").addEventListener("click", copyJson);
$("download-button").addEventListener("click", () => {
  if (!currentResult) return;
  const blob = new Blob([JSON.stringify(currentResult, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  const url = URL.createObjectURL(blob);
  link.href = url;
  link.download = "ktp_extraction.json";
  link.click();
  URL.revokeObjectURL(url);
});

loadConfig();
