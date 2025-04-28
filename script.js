let includeCompleted = false;
document.addEventListener("DOMContentLoaded", () => {
    const filterInput = document.getElementById("filter");

    backupLabels();
    updateColors();

    filterInput.addEventListener("input", (event) => {
        selectNodesNeighbourhood(event.target.value);
    });

    document.getElementById("checkbox")
    .addEventListener("change", (event) => {
        includeCompleted = event.target.checked;
        toggleCompletedCourses();
        if (includeCompleted) {
            selectNodesNeighbourhood(filterInput.value);
        }
    });

    toggleCompletedCourses();
});

function backupLabels() {
    for (let nodeId in allNodes) {
        if (allNodes[nodeId].label !== undefined) {
            allNodes[nodeId].savedLabel = allNodes[nodeId].label;
        }
    }
}

function updateColors() {
    let nodesToUpdate = [];

    let redNodes = new Set();
    let greenNodes = new Set(Object.keys(allNodes)
        .filter((node) =>
            !node.includes('OR') &&
            allNodes[node].color == "#00b200"))

    let nodeReqs = {};
    for (let edgeId in allEdges) {
        const { from: edgeFrom, to: edgeTo } = allEdges[edgeId];
        
        if (!redNodes.has(edgeFrom) && greenNodes.has(edgeFrom)) {    
            if (greenNodes.has(edgeTo) || edgeTo.includes('OR')) {
                allNodes[edgeFrom].color = "#b20000"
                nodeColors[edgeFrom] = "#b20000"
                nodesToUpdate.push(allNodes[edgeFrom]);
            } else {
                if (nodeReqs[edgeFrom] === undefined) {
                    nodeReqs[edgeFrom] = []
                }
                nodeReqs[edgeFrom].push(edgeTo)
            }
        }
    }
    nodes.update(nodesToUpdate);
}

function toggleCompletedCourses() {
    let updateArray = [];
    for (let nodeId in allNodes) {
        if (allNodes[nodeId].color === "#808080") {
            allNodes[nodeId].hidden = !includeCompleted;
            updateArray.push(allNodes[nodeId]);
        }
    }
    nodes.update(updateArray);
}

function selectNodesNeighbourhood(value) {
    let mainNodes = new Set(Object.keys(allNodes)
        .filter((node) => node.includes(value)));

    for (let nodeId in allNodes) {
        allNodes[nodeId].hidden = true;
        allNodes[nodeId].color = nodeColors[nodeId];
    }

    let neighbour1 = new Set();
    for (let nodeId of mainNodes) {
        allNodes[nodeId].hidden = false;
        allNodes[nodeId].color = nodeColors[nodeId];
        network.getConnectedNodes(nodeId).forEach((n) => neighbour1.add(n));
    }
    
    for (let nodeId of neighbour1) {
        if (allNodes[nodeId].hidden === false) {
            continue;
        }            
        allNodes[nodeId].hidden = false;
        allNodes[nodeId].color = `rgba(
            ${parseInt(nodeColors[nodeId].substring(1, 3), 16)}, 
            ${parseInt(nodeColors[nodeId].substring(3, 5), 16)}, 
            ${parseInt(nodeColors[nodeId].substring(5, 7), 16)}, 0.5)`;
    }
    
    var updateArray = [];
    for (let nodeId in allNodes) {
        if (allNodes[nodeId].hidden === false) {
            updateArray.push(allNodes[nodeId]);
        }
    }
    nodes.update(updateArray);
}