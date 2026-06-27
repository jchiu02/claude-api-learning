let portfolioData = [];

document.addEventListener("DOMContentLoaded", () => {
  fetch("/api/portfolios")
    .then((r) => r.json())
    .then((data) => {
      portfolioData = data.portfolios;
      populateDropdown();
    });

  document
    .getElementById("portfolio-select")
    .addEventListener("change", onPortfolioChange);
});

function populateDropdown() {
  const select = document.getElementById("portfolio-select");
  portfolioData.forEach((p) => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = p.name;
    select.appendChild(opt);
  });
}

function onPortfolioChange(e) {
  const id = e.target.value;
  const table = document.getElementById("positions-table");
  const empty = document.getElementById("empty-state");

  if (!id) {
    table.classList.add("hidden");
    empty.classList.remove("hidden");
    return;
  }

  empty.classList.add("hidden");
  table.classList.remove("hidden");

  const portfolio = portfolioData.find((p) => p.id === id);
  renderTable(portfolio);
}

function renderTable(portfolio) {
  const tbody = document.getElementById("positions-body");
  tbody.innerHTML = "";

  portfolio.bonds.forEach((bond, bondIdx) => {
    const bondPos = bond.positions.find((p) => p.type === "bond");
    const repos = bond.positions.filter((p) => p.type === "repo");
    const groupId = `bond-${bondIdx}`;

    // Parent row: net available
    const parentTr = document.createElement("tr");
    parentTr.className = "parent-row";
    parentTr.dataset.groupId = groupId;
    parentTr.addEventListener("click", () => toggleChildren(parentTr, groupId));

    let parentHtml =
      `<td><span class="chevron">&#9654;</span>${escHtml(bond.name)}</td>` +
      `<td>${escHtml(bond.isin)}</td>` +
      `<td><span class="type-badge net">Net Avail</span></td>` +
      `<td></td>`;

    for (let t = 0; t <= 5; t++) {
      const net = netAvailable(bond, t);
      const cls = net > 0 ? "positive" : net < 0 ? "negative" : "";
      parentHtml += `<td class="num ${cls}">${formatNum(net)}</td>`;
    }
    parentTr.innerHTML = parentHtml;
    tbody.appendChild(parentTr);

    // Children: repo positions (above bond)
    repos.forEach((repo) => {
      const repoTr = document.createElement("tr");
      repoTr.className = "child-row";
      repoTr.dataset.parentId = groupId;

      let repoHtml =
        `<td></td>` +
        `<td></td>` +
        `<td><span class="type-badge repo">Repo</span></td>` +
        `<td>${escHtml(repo.counterparty)}</td>`;

      for (let t = 0; t <= 5; t++) {
        const active = t < repo.repo_maturity_t;
        const val = active ? repo.notional : 0;
        const cls = active ? "negative" : "matured";
        repoHtml += `<td class="num ${cls}">${formatNum(val)}</td>`;
      }
      repoTr.innerHTML = repoHtml;
      tbody.appendChild(repoTr);
    });

    // Child: bond position (last, at the bottom)
    const bondTr = document.createElement("tr");
    bondTr.className = "child-row";
    bondTr.dataset.parentId = groupId;

    let bondHtml =
      `<td></td>` +
      `<td></td>` +
      `<td><span class="type-badge bond">Bond</span></td>` +
      `<td></td>`;

    for (let t = 0; t <= 5; t++) {
      bondHtml += `<td class="num positive">${formatNum(bondPos.notional)}</td>`;
    }
    bondTr.innerHTML = bondHtml;
    tbody.appendChild(bondTr);
  });
}

function netAvailable(bond, t) {
  const bondNotional = bond.positions.find((p) => p.type === "bond").notional;
  const activeRepoTotal = bond.positions
    .filter((p) => p.type === "repo" && t < p.repo_maturity_t)
    .reduce((sum, p) => sum + Math.abs(p.notional), 0);
  return bondNotional - activeRepoTotal;
}

function toggleChildren(parentTr, groupId) {
  const isExpanded = parentTr.classList.toggle("expanded");
  document.querySelectorAll(`tr[data-parent-id="${groupId}"]`).forEach((tr) => {
    tr.classList.toggle("visible", isExpanded);
  });
}

function formatNum(n) {
  if (n === 0) return "0";
  const abs = Math.abs(n);
  const formatted = abs.toLocaleString("en-GB");
  return n < 0 ? `(${formatted})` : formatted;
}

function escHtml(str) {
  if (!str) return "";
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
