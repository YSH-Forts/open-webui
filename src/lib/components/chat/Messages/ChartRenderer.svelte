<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
    import Chart from 'chart.js/auto';

    export let id: string;
    export let options: string;

    let canvas: HTMLCanvasElement;
    let chart: Chart;

    onMount(() => {
        try {
            const chartConfig = JSON.parse(options);
            chart = new Chart(canvas, chartConfig);
        } catch (error) {
            console.error('Failed to create chart:', error);
        }
    });

    onDestroy(() => {
        if (chart) {
            chart.destroy();
        }
    });
</script>

<div class="w-full h-full min-h-[300px] p-4">
    <canvas bind:this={canvas} id={`chart-${id}`}></canvas>
</div>

<style>
    canvas {
        width: 100% !important;
        height: 100% !important;
    }
</style> 