let includeCompleted = false;
document.addEventListener("DOMContentLoaded", () => {
    backupLabels();

    document.getElementById("filter")
    .addEventListener("input", (event) => {
        selectNodesNeighbourhood(event.target.value);
    });

    document.getElementById("checkbox")
    .addEventListener("change", (event) => {
        includeCompleted = event.target.checked;
        toggleCompletedCourses();
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

function toggleCompletedCourses() {
    for (let nodeId in allNodes) {
        let updateArray = [];

        if (allNodes[nodeId].color === "#808080") {
            allNodes[nodeId].hidden = !includeCompleted;
            updateArray.push(allNodes[nodeId]);
        }

        nodes.update(updateArray);
    }
}

function selectNodesNeighbourhood(value) {
    let mainNodes = Object.keys(allNodes)
        .filter((node) => node.includes(value))

    for (let nodeId in allNodes) {
        allNodes[nodeId].hidden = true;
        allNodes[nodeId].color = nodeColors[nodeId];
    }

    let neighbour1 = [];
    for (let nodeId of mainNodes) {
        allNodes[nodeId].hidden = false;
        allNodes[nodeId].color = nodeColors[nodeId];
        neighbour1.push(network.getConnectedNodes(nodeId));
    }
    
    for (let arr of neighbour1) {
        for (let nodeId of arr) {
            if (allNodes[nodeId].hidden === false) {
                continue;
            }
            
            allNodes[nodeId].hidden = false;
            allNodes[nodeId].color = `rgba(
            ${parseInt(nodeColors[nodeId].substring(1, 3), 16)}, 
            ${parseInt(nodeColors[nodeId].substring(3, 5), 16)}, 
            ${parseInt(nodeColors[nodeId].substring(5, 7), 16)}, 0.5)`;
        }
    }

    var updateArray = [];
    for (let nodeId in allNodes) {
        updateArray.push(allNodes[nodeId]);
    }

    nodes.update(updateArray);
}