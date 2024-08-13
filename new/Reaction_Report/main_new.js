function gotoeditorfun(arg) {
  var div = document.getElementById("framediv");
  div.classList.add("visible");
  var getbaritem = arg.value;
  localStorage.setItem("CompoundTurn", getbaritem);
  document.getElementById("compoudchangebarid").innerHTML =
    "Compound " + getbaritem;
}

function hideFrameDiv() {
  var div = document.getElementById("framediv");
  div.classList.remove("visible");
}

let reactantCount = 0;
let productCount = 0;

document.addEventListener("DOMContentLoaded", function () {

  const searchInput = document.getElementById("search-input");
  const suggestionsContainer = document.getElementById("suggestions");
  const rtnScheme = document.getElementById("Eqtn");
  const reactantRadio = document.getElementById("option1");
  const productRadio = document.getElementById("option2");
  const compoundImagesDiv = document.getElementById("compoundImages");
  

  searchInput.addEventListener("input", function () {
    const query = this.value.trim();
    // console.log(query);
    if (query.length === 0) {
      suggestionsContainer.innerHTML = "";
      return;
    }

    const apiUrl = `https://pubchem.ncbi.nlm.nih.gov/pcautocp/pcautocp.cgi?dict=pc_compoundnames&n=10&q=${encodeURIComponent(
      query
    )}`;

    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        displaySuggestions(data.autocp_array);
      })
      .catch((error) => console.error("Error:", error));
  });

  function displaySuggestions(suggestions) {
    suggestionsContainer.innerHTML = "";
    if (suggestions.length === 0) {
      return;
    }

    suggestions.forEach((suggestion) => {
      const a = document.createElement("a");
      a.href = "#";
      a.className = "list-group-item list-group-item-action suggestion-item";
      a.textContent = suggestion;
      a.addEventListener("click", function (e) {
        e.preventDefault();
        searchInput.value = suggestion;
        suggestionsContainer.innerHTML = "";
      });
      suggestionsContainer.appendChild(a);
    });
  }

  // Close suggestions when clicking outside
  document.addEventListener("click", function (event) {
    if (
      !suggestionsContainer.contains(event.target) &&
      event.target !== searchInput
    ) {
      suggestionsContainer.innerHTML = "";
    }
  });

  const searchButton = document.getElementById("search-button");
  searchButton.addEventListener("click", performSearch);

  async function performSearch() {

    const searchTerm = searchInput.value.trim();
    if (searchTerm.length === 0) {
      console.log("Please enter a search term");
      return;
    }

    try {
      // First API call to get CID
      const cidResponse = await fetch(
        `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/${encodeURIComponent(
          searchTerm
        )}/cids/json`
      );
      const cidData = await cidResponse.json();

      if (
        !cidData.IdentifierList ||
        !cidData.IdentifierList.CID ||
        cidData.IdentifierList.CID.length === 0
      ) {
        console.log("No CID found for the given compound");
        return;
      }

      const CID = cidData.IdentifierList.CID[0];
      console.log("CID Data:", cidData);
      // Second API call to get compound properties
      const propertiesResponse = await fetch(
        `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${CID}/property/MolecularFormula,MolecularWeight,HBondDonorCount,HBondAcceptorCount,IUPACName,CanonicalSMILES,IsomericSMILES,InChIKey,InChI/json`
      );
      const propertiesData = await propertiesResponse.json();
     
      // console.log('Properties Data:', propertiesData);

      // You can process the data further here if needed
      if (
        propertiesData.PropertyTable &&
        propertiesData.PropertyTable.Properties &&
        propertiesData.PropertyTable.Properties.length > 0
      ) {
        const properties = propertiesData.PropertyTable.Properties[0];
        console.log("Processed Properties:", {
          CID: properties.CID,
          MolecularFormula: properties.MolecularFormula,
          MolecularWeight: properties.MolecularWeight,
          CanonicalSMILES: properties.CanonicalSMILES,
          IsomericSMILES: properties.IsomericSMILES,
          InChI: properties.InChI,
          InChIKey: properties.InChIKey,
          IUPACName: properties.IUPACName,
          HBondDonorCount: properties.HBondDonorCount,
          HBondAcceptorCount: properties.HBondAcceptorCount,
        });

        let currentFormula = rtnScheme.value.trim();
        let newFormula = convertToSubscript(properties.MolecularFormula);

        if (currentFormula) {
          if (reactantRadio.checked) {
            // If reactant is selected, add to the left side
            if (currentFormula.includes("→")) {
              let [reactants, products] = currentFormula.split("→");
              reactants = reactants
                ? reactants + "  +  " + newFormula
                : newFormula;
              currentFormula = reactants + "  →  " + products;
            } else {
              currentFormula = currentFormula + "  +  " + newFormula;
            }
          } else if (productRadio.checked) {
            // If product is selected, add to the right side
            if (currentFormula.includes("→")) {
              let [reactants, products] = currentFormula.split("→");
              products = products
                ? products + "  +  " + newFormula
                : newFormula;
              currentFormula = reactants + "  →  " + products;
            } else {
              currentFormula = currentFormula + "  →  " + newFormula;
            }
          }
        } else {
          // If the input is empty, start a new reaction scheme
          currentFormula = reactantRadio.checked
            ? newFormula
            : "→  " + newFormula;
        }

        rtnScheme.value = currentFormula;


          // Create image container
        const createImageContainer = (imageUrl, formula, name) => {
          const imgContainer = document.createElement("div");
          imgContainer.style.display = "flex";
          imgContainer.style.flexDirection = "column";
          imgContainer.style.alignItems = "center";
          imgContainer.dataset.formula = convertToSubscript(formula);


          const imgElement = document.createElement("img");
          imgElement.src = imageUrl;
          imgElement.alt = name;
          imgElement.style.maxWidth = "150px";
      
          const formulaLabel = document.createElement("p");
          formulaLabel.textContent = convertToSubscript(formula);

          imgContainer.appendChild(imgElement);
          imgContainer.appendChild(formulaLabel);

          return imgContainer;
        };

        const createPlusSign = () => {
          const plusSign = document.createElement("div");
          plusSign.textContent = "+";
          plusSign.style.fontSize = "24px";
          plusSign.style.display = "flex";
          plusSign.style.alignItems = "center";
          return plusSign;
        };

        const addCompoundImage = (imageUrl, formula, name) => {
          const imgContainer = createImageContainer(imageUrl, formula, name);
          const compoundContainer = document.createElement("div");
          compoundContainer.style.display = "flex";
          compoundContainer.style.alignItems = "center";

          if (compoundImagesDiv.children.length === 0) {
            // First compound, just add it
            compoundContainer.appendChild(imgContainer);
            compoundImagesDiv.appendChild(compoundContainer);
          } else {
            if (reactantRadio.checked) {
              // Add to left side (before arrow if it exists)
              const arrow = compoundImagesDiv.querySelector('div[data-type="arrow"]');
              if (arrow) {
                compoundContainer.appendChild(createPlusSign());
                compoundContainer.appendChild(imgContainer);
                compoundImagesDiv.insertBefore(compoundContainer, arrow);
              } else {
                compoundContainer.appendChild(createPlusSign());
                compoundContainer.appendChild(imgContainer);
                compoundImagesDiv.appendChild(compoundContainer);
              }
            } else if (productRadio.checked) {
              // Add to right side
              let arrow = compoundImagesDiv.querySelector('div[data-type="arrow"]');
              if (!arrow) {
                // Create arrow if it doesn't exist
                arrow = document.createElement("div");
                arrow.textContent = "→";
                arrow.style.fontSize = "24px";
                arrow.style.margin = "auto 0px";
                arrow.dataset.type = "arrow";
                compoundImagesDiv.appendChild(arrow);
                compoundContainer.appendChild(imgContainer);
              } else {
                // Check if it's the first product after the arrow
                const firstProductAfterArrow = arrow.nextElementSibling === null;
                if (!firstProductAfterArrow) {
                  compoundContainer.appendChild(createPlusSign());
                }
                compoundContainer.appendChild(imgContainer);
              }
              compoundImagesDiv.appendChild(compoundContainer);
            }
          }
        };

        // In your main code, replace the image addition logic with:
        const imageUrl = `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${CID}/png`;
        addCompoundImage(imageUrl, properties.MolecularFormula, properties.IUPACName);

        const actualWgtInput = document.getElementById('actualWgt');
        
        if(reactantRadio.checked){
  
          addCompoundToTable(true,newFormula,properties.MolecularWeight,actualWgtInput.value)
        }else if(productRadio.checked){
          addCompoundToTable(false,newFormula,properties.MolecularWeight,actualWgtInput.value)
        }

        const formula = convertToSubscript(properties.MolecularFormula);
      
      addCompoundToKeyword(searchTerm,formula)

      }






    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
});


function removeCompoundFromScheme(formula) {
  const rtnScheme = document.getElementById("Eqtn");
  let currentFormula = rtnScheme.value.trim();
  
  currentFormula = currentFormula.replace(formula + "  +  ", "");
  currentFormula = currentFormula.replace("  +  " + formula, "");
  currentFormula = currentFormula.replace(formula, "");
  
  // Clean up any leftover arrows or plus signs
  currentFormula = currentFormula.replace("→  ", "→");
  currentFormula = currentFormula.replace("  →", "→");
  currentFormula = currentFormula.replace("  +  ", " + ");
  currentFormula = currentFormula.trim();
  
  // Update the reaction scheme
  rtnScheme.value = currentFormula;
}

function removeCompoundImage(formula) {
  const compoundImagesDiv = document.getElementById('compoundImages');
  const imgContainers = compoundImagesDiv.querySelectorAll('div[data-formula]');
  
  for (let container of imgContainers) {
    if (container.dataset.formula === formula) {
      const parentContainer = container.parentElement;
      
      // Remove the plus sign if it exists
      if (parentContainer.previousElementSibling && parentContainer.previousElementSibling.textContent === '+') {
        parentContainer.previousElementSibling.remove();
      } else if (parentContainer.nextElementSibling && parentContainer.nextElementSibling.textContent === '+') {
        parentContainer.nextElementSibling.remove();
      }
      
      // Remove the container
      parentContainer.remove();
      
      // If there are no more compounds, remove the arrow
      const arrow = compoundImagesDiv.querySelector('div[data-type="arrow"]');
      if (arrow && compoundImagesDiv.children.length <= 1) {
        arrow.remove();
      }
      
      break;
    }
  }
}


function addCompoundToKeyword(value,formula) {
  
  const newSpan = document.createElement('span');
  newSpan.className = 'filter';
  newSpan.textContent = value + " ";

  const icon = document.createElement('i');
  icon.className = 'fa-solid fa-xmark';

  newSpan.appendChild(icon);

  newSpan.addEventListener('click', function() {
    this.remove(); // Remove the span when clicked
    removeCompoundFromScheme(formula);
    removeCompoundFromTable(formula);
    removeCompoundImage(formula);
  });
  document.querySelector('.keyword-filters').appendChild(newSpan);
}


function removeCompoundFromTable(formula) {
  const table = document.querySelector('.table-bordered');
  const rows = table.querySelectorAll('tr');
  
  for (let row of rows) {
    const formulaInput = row.querySelector('.molecular-formula');
    if (formulaInput && formulaInput.value === formula) {
      row.remove();
      break;
    }
  }

  updateRatios(table);

  updateCompoundCounts();
}

function updateCompoundCounts() {
  const table = document.querySelector('.table-bordered');
  const rows = table.querySelectorAll('tr');
   reactantCount = 0;
   productCount = 0;
  
  for (let row of rows) {
    const typeInput = row.querySelector('input[type="button"]');
    if (typeInput) {
      if (typeInput.value.startsWith('R')) {
        reactantCount++;
        typeInput.value = `R${reactantCount}`;
      } else if (typeInput.value.startsWith('P')) {
        productCount++;
        typeInput.value = `P${productCount}`;
      }
    }
  }
}



function convertToSubscript(formula) {
  const subscriptMap = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'
  };
  
  return formula.replace(/(\d+)/g, match => {
    return match.split('').map(digit => subscriptMap[digit] || digit).join('');
  });
}

function addCompoundToTable(isReactant,MolecularFormula,MolecularWeight,actualWgt) {
  
  const table = document.querySelector('.table-bordered');
  const newRow = document.createElement('tr');
  const compoundType = isReactant ? 'R' : 'P';
  const compoundNumber = isReactant ? ++reactantCount : ++productCount;
  console.log(actualWgt)
  let moles = (actualWgt / MolecularWeight).toFixed(2);


  newRow.innerHTML = `
      <td><input type="button" class="${isReactant ? 'reactant-btn' : 'product-btn'}" value="${compoundType}${compoundNumber}" readonly></td>
      <td><input type="text" class="molecular-formula" value="${MolecularFormula}" ></td>
      <td><input type="text" class="molecular-weight"  value="${MolecularWeight}"  ></td>
      <td><input type="text" class="chemical-weight" value="${actualWgt}" ></td>
      <td><input type="text" class="moles"  value="${moles}" ></td>
      <td><input type="text" class="ratio"  ></td>
      <td><input type="text" class="density"></td>
  `;

  if (isReactant) {
    // Find the first product row or the end of the table
    const firstProductRow = Array.from(table.rows).find(row => {
      const input = row.cells[0].querySelector('input');
      return input && input.value.startsWith('P');
  });
    if (firstProductRow) {
        table.insertBefore(newRow, firstProductRow);
    } else {
        table.appendChild(newRow);
    }
} else {
    table.appendChild(newRow);
}
  updateRatios(table);
}

function updateRatios(table) {
  const rows = Array.from(table.rows).slice(1); // Skip header row
  
  const reactants = rows.filter(row => {
    const input = row.cells[0]?.querySelector('input');
    return input && input.value.startsWith('R');
  });
  
  const products = rows.filter(row => {
    const input = row.cells[0]?.querySelector('input');
    return input && input.value.startsWith('P');
  });

  function calculateRatios(compounds) {
    if (compounds.length === 0) return;
    
    const moles = compounds.map(row => {
      const input = row.cells[4]?.querySelector('input');
      return input ? parseFloat(input.value) : 0;
    }).filter(value => !isNaN(value));

    const totalMoles = moles.reduce((sum, value) => sum + value, 0);
    
    if (totalMoles === 0) return;

    compounds.forEach((row) => {
      const moleInput = row.cells[4]?.querySelector('input');
      const ratioInput = row.cells[5]?.querySelector('input');
      if (moleInput && ratioInput) {
        const mole = parseFloat(moleInput.value);
        if (!isNaN(mole)) {
          const ratio = (mole / totalMoles).toFixed(2);
          ratioInput.value = ratio;
        }
      }
    });
  }

  calculateRatios(reactants);
  calculateRatios(products);
}