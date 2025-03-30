<script lang="ts">
	import { marked } from 'marked';
	import { replaceTokens, processResponseContent } from '$lib/utils';
	import { user } from '$lib/stores';

	import markedExtension from '$lib/utils/marked/extension';
	import markedKatexExtension from '$lib/utils/marked/katex-extension';

	import MarkdownTokens from './Markdown/MarkdownTokens.svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let id: string;
	export let content: string;
	export let model: any = null;
	export let save = false;

	export let sourceIds: string[] = [];

	export let onSourceClick: Function = () => {};
	export let onTaskClick: Function = () => {};

	let tokens: any[] = [];

	const options = {
		throwOnError: false
	};

	marked.use(markedKatexExtension(options));
	marked.use(markedExtension(options));

	// 预处理 Markdown 内容，将 echarts 代码块转换为标准代码块
	function preprocessECharts(content: string): string {
		// 保持 ```echarts 代码块不变，确保标记为 echarts 语言
		return content.replace(/```echarts\s+([\s\S]+?)```/g, (match: string, code: string) => {
			return "```echarts\n" + code + "\n```";
		});
	}

	$: (async () => {
		if (content) {
			// 预处理 echarts 代码块
			const processedContent = preprocessECharts(content);
			tokens = marked.lexer(
				replaceTokens(processResponseContent(processedContent), sourceIds, model?.name, $user?.name)
			);
		}
	})();
</script>

{#key id}
	<MarkdownTokens
		{tokens}
		{id}
		{save}
		{onTaskClick}
		{onSourceClick}
		on:update={(e) => {
			dispatch('update', e.detail);
		}}
		on:code={(e) => {
			dispatch('code', e.detail);
		}}
	/>
{/key}
