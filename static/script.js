document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const analysisForm = document.getElementById('analysisForm');
    const uploadStatus = document.getElementById('uploadStatus');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const statsCard = document.getElementById('statsCard');

    // Handle file upload
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData();
        const fileInput = document.getElementById('csvFile');
        formData.append('file', fileInput.files[0]);

        uploadStatus.innerHTML = '<div class="alert alert-info"><i class="fas fa-spinner fa-spin"></i> Uploading and processing file...</div>';

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                uploadStatus.innerHTML = '<div class="alert alert-success"><i class="fas fa-check"></i> ' + result.success + '</div>';
                analyzeBtn.disabled = false;
                loadStats();
            } else {
                uploadStatus.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> ' + result.error + '</div>';
            }
        } catch (error) {
            uploadStatus.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> Error uploading file</div>';
        }
    });

    // Handle analysis
    analysisForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const support = document.getElementById('minSupport').value;
        const metric = document.getElementById('metric').value;
        const threshold = document.getElementById('minThreshold').value;

        analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
        analyzeBtn.disabled = true;

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    support: support,
                    metric: metric,
                    threshold: threshold
                })
            });
            
            const result = await response.json();
            
            if (result.error) {
                document.getElementById('frequentItemsets').innerHTML = 
                    '<div class="alert alert-warning"><i class="fas fa-exclamation-triangle"></i> ' + result.error + '</div>';
            } else {
                displayFrequentItemsets(result.frequent_itemsets);
                displayAssociationRules(result.association_rules);
            }
        } catch (error) {
            document.getElementById('frequentItemsets').innerHTML = 
                '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> Error during analysis</div>';
        } finally {
            analyzeBtn.innerHTML = '<i class="fas fa-chart-line"></i> Run Analysis';
            analyzeBtn.disabled = false;
        }
    });

    async function loadStats() {
        try {
            const response = await fetch('/stats');
            const stats = await response.json();
            
            if (!stats.error) {
                document.getElementById('statsContent').innerHTML = `
                    <div class="row">
                        <div class="col-6 stats-item">
                            <div class="stats-number">${stats.total_images.toLocaleString()}</div>
                            <div class="stats-label">Total Images</div>
                        </div>
                        <div class="col-6 stats-item">
                            <div class="stats-number">${stats.unique_findings}</div>
                            <div class="stats-label">Unique Findings</div>
                        </div>
                    </div>
                    <div class="mt-3">
                        <h6>Available Findings:</h6>
                        <div class="d-flex flex-wrap">
                            ${stats.findings_list.map(finding => 
                                `<span class="badge bg-secondary me-1 mb-1">${finding}</span>`
                            ).join('')}
                        </div>
                    </div>
                `;
                statsCard.style.display = 'block';
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    function displayFrequentItemsets(itemsets) {
        if (!itemsets || itemsets.length === 0) {
            document.getElementById('frequentItemsets').innerHTML = 
                '<div class="alert alert-info">No frequent itemsets found with current parameters</div>';
            return;
        }

        let html = '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>Itemset</th><th>Support</th></tr></thead><tbody>';
        
        itemsets.forEach(item => {
            html += `<tr>
                <td>
                    ${item.itemsets.map(i => `<span class="badge bg-primary itemset-badge">${i}</span>`).join('')}
                </td>
                <td><span class="metric-value">${item.support}</span></td>
            </tr>`;
        });
        
        html += '</tbody></table></div>';
        document.getElementById('frequentItemsets').innerHTML = html;
    }

    function displayAssociationRules(rules) {
        if (!rules || rules.length === 0) {
            document.getElementById('associationRules').innerHTML = 
                '<div class="alert alert-info">No association rules found with current parameters</div>';
            return;
        }

        let html = '<div class="table-responsive"><table class="table table-striped"><thead><tr><th>Rule</th><th>Support</th><th>Confidence</th><th>Lift</th></tr></thead><tbody>';
        
        rules.forEach(rule => {
            html += `<tr>
                <td>
                    ${rule.antecedents.map(a => `<span class="badge bg-info itemset-badge">${a}</span>`).join('')}
                    <span class="rule-arrow">→</span>
                    ${rule.consequents.map(c => `<span class="badge bg-success itemset-badge">${c}</span>`).join('')}
                </td>
                <td><span class="metric-value">${rule.support}</span></td>
                <td><span class="metric-value">${rule.confidence}</span></td>
                <td><span class="metric-value">${rule.lift}</span></td>
            </tr>`;
        });
        
        html += '</tbody></table></div>';
        document.getElementById('associationRules').innerHTML = html;
    }
});