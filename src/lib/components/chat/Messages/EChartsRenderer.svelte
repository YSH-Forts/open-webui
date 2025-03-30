<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import type { ECharts } from 'echarts';
    import * as echarts from 'echarts';

    export let options: string;
    export let id: string;
    export let height = '400px';

    let chart: ECharts | undefined;
    let chartContainer: HTMLDivElement;

    function parseEChartsOptions(optionsStr: string): any {
        let parsedOptions;
        
        // If the options string contains 'echarts' references, safely evaluate it
        if (optionsStr.includes('echarts.')) {
            try {
                // Replace 'echarts.' with the actual echarts object
                const evalStr = optionsStr.replace(/echarts\./g, 'window.echarts.');
                // Make echarts available in window scope
                (window as any).echarts = echarts;
                // Safely evaluate the string
                parsedOptions = eval('(' + evalStr + ')');
            } catch (err) {
                console.error('Error evaluating ECharts options:', err);
                throw err;
            }
        } else {
            // If no echarts references, try normal JSON parse
            try {
                parsedOptions = JSON.parse(optionsStr);
            } catch (err) {
                console.error('Error parsing JSON options:', err);
                throw err;
            }
        }

        // Add tooltip if not present
        if (!parsedOptions.tooltip) {
            parsedOptions.tooltip = {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            };
        }

        // Add toolbox if not present
        if (!parsedOptions.toolbox) {
            parsedOptions.toolbox = {
                show: true,
                feature: {
                    dataView: { 
                        show: true, 
                        readOnly: false,
                        title: '数据视图',
                        lang: ['数据视图', '关闭', '刷新'],
                        backgroundColor: '#fff',
                        textareaColor: '#fff',
                        textareaBorderColor: '#e5e7eb',
                        textColor: '#333',
                        buttonColor: '#1890ff',
                        buttonTextColor: '#fff',
                        optionToContent: (opt: any) => {
                            let axisData = opt.xAxis?.[0]?.data || [];
                            let series = opt.series || [];
                            
                            // Create table header
                            let table = '<table style="width:100%;border-collapse:collapse;margin:10px 0;text-align:center">';
                            table += '<thead><tr style="background-color:#f5f5f5">' +
                                '<th style="padding:12px;border:1px solid #e5e7eb">类别</th>';
                            
                            // Add series names as headers
                            series.forEach((s: any) => {
                                table += `<th style="padding:12px;border:1px solid #e5e7eb">${s.name || ''}</th>`;
                            });
                            table += '</tr></thead><tbody>';
                            
                            // Add data rows
                            axisData.forEach((category: string, index: number) => {
                                table += '<tr>';
                                table += `<td style="padding:12px;border:1px solid #e5e7eb">${category}</td>`;
                                series.forEach((s: any) => {
                                    let value = s.data[index];
                                    if (typeof value === 'object' && value !== null) {
                                        value = value.value; // Handle object format data
                                    }
                                    table += `<td style="padding:12px;border:1px solid #e5e7eb">${value}</td>`;
                                });
                                table += '</tr>';
                            });
                            
                            table += '</tbody></table>';
                            return table;
                        },
                        contentToOption: (content: string) => {
                            // Parse table content back to option
                            try {
                                const parser = new DOMParser();
                                const doc = parser.parseFromString(content, 'text/html');
                                const rows = doc.querySelectorAll('tr');
                                const headers = Array.from(rows[0].querySelectorAll('th'));
                                const seriesNames = headers.slice(1).map(th => th.textContent || '');
                                
                                const data: any = {
                                    xAxis: [{ data: [] }],
                                    series: seriesNames.map(name => ({
                                        name,
                                        data: []
                                    }))
                                };
                                
                                // Skip header row
                                for (let i = 1; i < rows.length; i++) {
                                    const cells = rows[i].querySelectorAll('td');
                                    data.xAxis[0].data.push(cells[0].textContent || '');
                                    
                                    for (let j = 1; j < cells.length; j++) {
                                        const value = cells[j].textContent || '';
                                        data.series[j-1].data.push(parseFloat(value) || value);
                                    }
                                }
                                
                                return data;
                            } catch (error) {
                                console.error('Error parsing table content:', error);
                                return parsedOptions;
                            }
                        }
                    },
                    restore: {
                        show: true,
                        title: '还原'
                    },
                    saveAsImage: {
                        show: true,
                        title: '保存为图片'
                    }
                }
            };
        }

        return parsedOptions;
    }

    onMount(() => {
        if (chartContainer) {
            try {
                chart = echarts.init(chartContainer);
                const parsedOptions = parseEChartsOptions(options);
                chart.setOption(parsedOptions);
                console.log('ECharts initialized successfully with options:', parsedOptions);

                const resizeHandler = () => {
                    chart?.resize();
                };

                window.addEventListener('resize', resizeHandler);

                return () => {
                    window.removeEventListener('resize', resizeHandler);
                    chart?.dispose();
                };
            } catch (err) {
                const error = err as Error;
                console.error('Error initializing ECharts:', error);
                chartContainer.innerHTML = `<div style="color: red; padding: 10px;">Error rendering chart: ${error.message}</div>`;
            }
        }
    });

    onDestroy(() => {
        if (chart) {
            chart.dispose();
        }
    });
</script>

<div bind:this={chartContainer} {id} style="width: 100%; height: {height};" />

<style>
    div {
        margin: 1rem 0;
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
    }
</style> 