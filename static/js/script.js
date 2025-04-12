// script.js
$(document).ready(function() {
    // Graph state
    let nodes = [];
    let autoRunInterval = null;

    // UI element handlers
    $('#graphType').change(function() {
        if ($(this).val() === 'custom') {
            $('#customGraphOptions').show();
            $('#predefinedGraphOptions').hide();
        } else {
            $('#customGraphOptions').hide();
            $('#predefinedGraphOptions').show();
        }
    });

    $('#executionSpeed').on('input', function() {
        const speedValue = ($(this).val() / 1000).toFixed(1);
        $('#speedValue').text(speedValue);
    });

    // Create graph button
    $('#createGraphBtn').click(function() {
        const graphType = $('#graphType').val();
        let data = {
            graph_type: graphType
        };

        if (graphType === 'custom') {
            data.edge_list = $('#edgeList').val();
        } else {
            data.size = $('#graphSize').val();
        }

        // Reset BFS UI
        resetBfsUI();

        // Send request to create graph
        $.ajax({
            url: '/create_graph',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function(response) {
                if (response.success) {
                    // Update graph visualization
                    updateGraphVisualization(response.graph_image);
                    
                    // Update nodes for BFS starting point selection
                    nodes = response.nodes;
                    updateStartNodeDropdown();
                    
                    // Show algorithm controls
                    $('#algorithmControlsCard').show();
                }
            },
            error: function(error) {
                console.error('Error creating graph:', error);
            }
        });
    });

    // Start BFS button
    $('#startBfsBtn').click(function() {
        const startNode = $('#startNode').val();
        
        // Send request to initialize BFS
        $.ajax({
            url: '/initialize_bfs',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ start_node: startNode }),
            success: function(response) {
                if (response.success) {
                    // Update visualization
                    updateGraphVisualization(response.graph_image);
                    
                    // Update BFS status
                    updateBFSStatus(response.state);
                    
                    // Update UI controls
                    $('#startBfsBtn').prop('disabled', true);
                    $('#stepBfsBtn').prop('disabled', false);
                    $('#completeBfsBtn').prop('disabled', false);
                    $('#resetBfsBtn').prop('disabled', false);
                    
                    // Highlight pseudocode
                    highlightPseudocode(1);
                }
            },
            error: function(error) {
                console.error('Error initializing BFS:', error);
            }
        });
    });

    // Step BFS button
    $('#stepBfsBtn').click(function() {
        stepBFS();
    });

    // Auto-complete BFS button
    $('#completeBfsBtn').click(function() {
        // Send request to complete BFS
        $.ajax({
            url: '/complete_bfs',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({}),
            success: function(response) {
                if (response.success) {
                    // Update visualization
                    updateGraphVisualization(response.graph_image);
                    
                    // Update BFS status
                    updateBFSStatus(response.state);
                    
                    // Update UI controls if BFS is finished
                    if (response.state.finished) {
                        $('#stepBfsBtn').prop('disabled', true);
                        $('#completeBfsBtn').prop('disabled', true);
                    }
                }
            },
            error: function(error) {
                console.error('Error completing BFS:', error);
            }
        });
    });

    // Reset BFS button
    $('#resetBfsBtn').click(function() {
        resetBfsUI();
    });

    // Helper functions
    function updateStartNodeDropdown() {
        const $dropdown = $('#startNode');
        $dropdown.empty();
        
        nodes.forEach(node => {
            $dropdown.append($('<option>', {
                value: node,
                text: node
            }));
        });
    }

    function updateGraphVisualization(imageData) {
        const $container = $('#graphContainer');
        $container.empty();
        
        if (imageData) {
            const $img = $('<img>', {
                src: 'data:image/png;base64,' + imageData,
                alt: 'Graph Visualization'
            });
            $container.append($img);
        } else {
            $container.html('<p class="text-muted">No graph available</p>');
        }
    }

    function updateBFSStatus(state) {
        $('#currentNode').text(state.current_node || '-');
        $('#visitedNodes').text(state.visited.join(', ') || '-');
        $('#nodeQueue').text(state.queue.join(', ') || '-');
        $('#stepCount').text(state.step_count);
        
        // Determine which pseudocode step to highlight
        if (state.step_count === 0) {
            // BFS just initialized
            highlightPseudocode(2);
        } else if (state.queue.length === 0 && state.finished) {
            // BFS completed
            highlightPseudocode(0);
        } else {
            // BFS in progress
            if (state.queue.length > 0) {
                highlightPseudocode(3);
            } else {
                highlightPseudocode(3, 'a');
            }
        }
    }

    function highlightPseudocode(step, substep = null) {
        // Remove all highlighting
        $('#pseudocode').find('.current-step').removeClass('current-step');
        $('#pseudocode').find('.completed-step').removeClass('completed-step');
        
        let selector = '';
        
        if (step === 0) {
            // All steps completed
            $('#pseudocode').find('li').addClass('completed-step');
            return;
        } else if (step === 1) {
            selector = '#pseudocode li:nth-child(1)';
        } else if (step === 2) {
            selector = '#pseudocode li:nth-child(2)';
        } else if (step === 3) {
            if (substep === 'a') {
                selector = '#pseudocode li:nth-child(3) li:nth-child(1)';
            } else if (substep === 'b') {
                selector = '#pseudocode li:nth-child(3) li:nth-child(2)';
            } else {
                selector = '#pseudocode li:nth-child(3)';
            }
        }
        
        // Add highlighting to current step
        $(selector).addClass('current-step');
        
        // Mark previous steps as completed
        for (let i = 1; i < step; i++) {
            $(`#pseudocode li:nth-child(${i})`).addClass('completed-step');
        }
    }

    function stepBFS() {
        // Send request to step BFS
        $.ajax({
            url: '/step_bfs',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({}),
            success: function(response) {
                if (response.success) {
                    // Update visualization
                    updateGraphVisualization(response.graph_image);
                    
                    // Update BFS status
                    updateBFSStatus(response.state);
                    
                    // Update UI controls if BFS is finished
                    if (response.state.finished) {
                        $('#stepBfsBtn').prop('disabled', true);
                        $('#completeBfsBtn').prop('disabled', true);
                    }
                }
            },
            error: function(error) {
                console.error('Error stepping BFS:', error);
            }
        });
    }

    function resetBfsUI() {
        // Clear BFS status
        $('#currentNode').text('-');
        $('#visitedNodes').text('-');
        $('#nodeQueue').text('-');
        $('#stepCount').text('0');
        
        // Reset UI controls
        $('#startBfsBtn').prop('disabled', false);
        $('#stepBfsBtn').prop('disabled', true);
        $('#completeBfsBtn').prop('disabled', true);
        $('#resetBfsBtn').prop('disabled', true);
        
        // Clear pseudocode highlighting
        $('#pseudocode').find('.current-step').removeClass('current-step');
        $('#pseudocode').find('.completed-step').removeClass('completed-step');
        
        // Clear interval if auto-running
        if (autoRunInterval) {
            clearInterval(autoRunInterval);
            autoRunInterval = null;
        }
    }
});