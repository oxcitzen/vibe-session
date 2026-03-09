const form = document.getElementById("recipe-form");
const ingredientsEl = document.getElementById("ingredients");
const clearBtn = document.getElementById("clear-btn");
const submitBtn = document.getElementById("submit-btn");
const copyBtn = document.getElementById("copy-btn");

const loadingEl = document.getElementById("loading");
const errorEl = document.getElementById("error");
const recipesEl = document.getElementById("recipes");
const jsonOutputEl = document.getElementById("json-output");

function setLoading(isLoading) {
  if (isLoading) {
    loadingEl.classList.remove("hidden");
    submitBtn.disabled = true;
  } else {
    loadingEl.classList.add("hidden");
    submitBtn.disabled = false;
  }
}

function showError(message) {
  if (!message) {
    errorEl.classList.add("hidden");
    errorEl.textContent = "";
    return;
  }
  errorEl.textContent = message;
  errorEl.classList.remove("hidden");
}

function escapeHtml(s) {
  const div = document.createElement("div");
  div.textContent = s;
  return div.innerHTML;
}

function renderRecipe(recipe) {
  const name = escapeHtml(recipe.name || "Untitled recipe");
  const cookingTime = escapeHtml(recipe.cookingTime || "");
  const difficulty = escapeHtml(recipe.difficulty || "");
  const calories =
    recipe.nutrition && typeof recipe.nutrition.calories !== "undefined"
      ? `${recipe.nutrition.calories} kcal`
      : "";
  const protein = recipe.nutrition?.protein ? escapeHtml(recipe.nutrition.protein) : "";
  const carbs = recipe.nutrition?.carbs ? escapeHtml(recipe.nutrition.carbs) : "";

  const ingredients = Array.isArray(recipe.ingredients) ? recipe.ingredients : [];
  const instructions = Array.isArray(recipe.instructions) ? recipe.instructions : [];

  const ingList = ingredients
    .map((i) => `<li>${escapeHtml(String(i))}</li>`)
    .join("");

  const instList = instructions
    .map((i) => `<li>${escapeHtml(String(i))}</li>`)
    .join("");

  return `
    <article class="recipe">
      <h3>${name}</h3>
      <div class="meta">
        ${cookingTime ? `<span class="pill"><strong>Time</strong> ${cookingTime}</span>` : ""}
        ${difficulty ? `<span class="pill"><strong>Difficulty</strong> ${difficulty}</span>` : ""}
        ${calories ? `<span class="pill"><strong>Calories</strong> ${escapeHtml(calories)}</span>` : ""}
        ${protein ? `<span class="pill"><strong>Protein</strong> ${protein}</span>` : ""}
        ${carbs ? `<span class="pill"><strong>Carbs</strong> ${carbs}</span>` : ""}
      </div>

      <div class="section-title">Ingredients</div>
      <ul>${ingList || "<li>(none)</li>"}</ul>

      <div class="section-title">Instructions</div>
      <ol>${instList || "<li>(none)</li>"}</ol>
    </article>
  `;
}

function setJsonOutput(obj) {
  const text = JSON.stringify(obj, null, 2);
  jsonOutputEl.textContent = text;
  jsonOutputEl.classList.remove("hidden");
  copyBtn.classList.remove("hidden");
}

function clearOutput() {
  recipesEl.innerHTML = "";
  jsonOutputEl.textContent = "";
  jsonOutputEl.classList.add("hidden");
  copyBtn.classList.add("hidden");
}

async function postRecipes(ingredients) {
  const res = await fetch("/api/recipes", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ingredients }),
  });

  const contentType = res.headers.get("content-type") || "";
  const isJson = contentType.includes("application/json");
  const data = isJson ? await res.json() : await res.text();

  if (!res.ok) {
    // FastAPI returns {"detail": "..."} on HTTPException
    const message =
      typeof data === "object" && data && data.detail
        ? String(data.detail)
        : "Request failed";
    throw new Error(message);
  }

  return data;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  showError("");
  clearOutput();

  const ingredients = (ingredientsEl.value || "").trim();
  if (!ingredients) {
    showError("Please enter at least one ingredient.");
    return;
  }

  setLoading(true);
  try {
    const data = await postRecipes(ingredients);
    setJsonOutput(data);

    const recipes = Array.isArray(data.recipes) ? data.recipes : [];
    recipesEl.innerHTML = recipes.map(renderRecipe).join("");
  } catch (err) {
    showError(err?.message || "Something went wrong.");
  } finally {
    setLoading(false);
  }
});

clearBtn.addEventListener("click", () => {
  ingredientsEl.value = "";
  showError("");
  clearOutput();
  ingredientsEl.focus();
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(jsonOutputEl.textContent || "");
    copyBtn.textContent = "Copied!";
    setTimeout(() => (copyBtn.textContent = "Copy JSON"), 900);
  } catch {
    copyBtn.textContent = "Copy failed";
    setTimeout(() => (copyBtn.textContent = "Copy JSON"), 900);
  }
});

