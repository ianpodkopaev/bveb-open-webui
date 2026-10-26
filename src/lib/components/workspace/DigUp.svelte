<script lang="ts">
	import { onMount, getContext } from 'svelte';
	const i18n = getContext('i18n');

	import { user } from '$lib/stores';
	import { toast } from 'svelte-sonner';
	import {
		digupStatus,
		digupSearch,
		digupText,
		digupRender,
		type DigUpHit
	} from '$lib/apis/digup';
	import Tooltip from '../common/Tooltip.svelte';
	import Spinner from '../common/Spinner.svelte';

	let status: any = null;
	let statusError: string | null = null;

	let query = '';
	let code = false;
	let busy = false;
	let hits: DigUpHit[] = [];
	let meaning = false;
	let searched = false;
	let ms: { embed?: number; search?: number } | null = null;

	let expanded: Record<string, string | null> = {};
	// path|loc -> image url; null = preview rendering; false = no preview
	let thumbs: Record<string, string | null | false> = {};

	const token = () => localStorage.token;

	const mediaUrl = (path: string) => `/api/v1/digup/media?path=${encodeURIComponent(path)}`;

	const runSearch = async (e?: Event) => {
		e?.preventDefault();
		const q = query.trim();
		if (!q || busy) return;
		busy = true;
		try {
			const res = await digupSearch(token(), { q, code, limit: 12 });
			hits = res.hits ?? [];
			meaning = !!res.meaning;
			ms = res.ms ?? null;
			searched = true;
			if (res.warning) toast.message(res.warning);
			hits.forEach(ensureThumb);
			hits.forEach(ensureText);
		} catch (err: any) {
			toast.error(typeof err === 'string' ? err : err?.detail ?? 'DigUp search failed');
		} finally {
			busy = false;
		}
	};

	// A picture for a hit: originals (images) show straight away; everything
	// else (PDF page, video frame, screenshot, HEIC…) is rendered by the bridge.
	function ensureThumb(h: DigUpHit) {
		const key = h.path + '|' + (h.loc ?? '');
		if (thumbs[key] !== undefined) return;
		if (h.kind === 'image') {
			thumbs[key] = mediaUrl(h.path);
			return;
		}
		thumbs[key] = null;   // null = “rendered preview still loading”
		if (!['pdf', 'video', 'screenshot'].includes(h.kind)) return;
		digupRender(token(), { path: h.path, kind: h.kind, loc: h.loc, pixels: 480 })
			.then((r) => {
				if (r?.image) thumbs[key] = mediaUrl(r.image);
			})
			.catch(() => (thumbs[key] = false));
	}

	// Code hits: pull the source stretch the answer is made of.
	function ensureText(h: DigUpHit) {
		if (h.kind !== 'code' || expanded[h.path + h.loc] !== undefined) return;
		if (h.excerpt) return expanded[h.path + h.loc] = h.excerpt;
		digupText(token(), { segment: h.segment_id, code: true })
			.then((r) => (expanded[h.path + h.loc] = r?.text ?? ''))
			.catch(() => (expanded[h.path + h.loc] = ''));
	}

	onMount(async () => {
		try {
			status = await digupStatus(token());
		} catch (err: any) {
			statusError =
				'DigUp service is unreachable on this host (' +
				(typeof err === 'string' ? err : err?.detail ?? 'bridge not running') +
				').';
		}
	});
</script>

<div class="max-w-4xl">
	<div class="mb-4 flex flex-wrap items-center gap-x-6 gap-y-1 text-sm text-gray-500 dark:text-gray-400">
		<span class="font-medium text-gray-900 dark:text-gray-100">DigUp</span>
		{#if status}
			<span>{status.searchable ?? 0} files indexed</span>
			{#if status.code_vectors}
				<span>· {status.code_vectors} code stretches</span>
			{/if}
			<span>· encoder: {status.encoder ?? 'cold'}</span>
		{:else if statusError}
			<span class="text-red-500">{statusError}</span>
		{/if}
	</div>

	<form class="flex flex-col gap-2 sm:flex-row" on:submit={runSearch}>
		<div class="flex-1">
			<input
				bind:value={query}
				placeholder="Describe what you are looking for — “the dog on the beach”, “where the token is validated”…"
				class="w-full rounded-lg border border-gray-200 bg-white px-4 py-3 text-sm text-gray-900 outline-none placeholder:text-gray-400 focus:border-gray-400 dark:border-gray-700 dark:bg-gray-900 dark:text-gray-100"
			/>
		</div>
		<label class="flex select-none items-center gap-2 self-center text-sm text-gray-700 dark:text-gray-300">
			<input type="checkbox" bind:checked={code} class="accent-gray-900 dark:accent-gray-100" />
			code
		</label>
		<button
			type="submit"
			disabled={busy || !query.trim() || !!statusError}
			class="inline-flex items-center justify-center gap-2 rounded-lg bg-gray-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40 dark:bg-gray-100 dark:text-gray-900 dark:hover:bg-white"
		>
			{#if busy}<Spinner />{/if}
			{$i18n.t('Search')}
		</button>
	</form>

	{#if searched}
		<div class="mt-2 text-xs text-gray-400 dark:text-gray-500">
			{hits.length} result{hits.length === 1 ? '' : 's'}
			{#if ms}
				· embed {ms.embed ?? 0} ms + search {ms.search ?? 0} ms
			{/if}
			{#if !meaning && query.trim()}
				· <span class="text-amber-500">meaning search off (encoder unavailable) — keywords only</span>
			{/if}
		</div>
	{/if}

	{#if hits.length}
		<ul class="mt-4 space-y-3">
			{#each hits as h (h.path + h.loc)}
				{@const key = h.path + '|' + (h.loc ?? '')}
				{@const codeKey = h.path + h.loc}
				<li
					class="flex gap-4 rounded-xl border border-gray-200 bg-white p-4 transition hover:border-gray-300 dark:border-gray-700 dark:bg-gray-900/40 dark:hover:border-gray-600"
				>
					<div
						class="h-24 w-36 flex-none overflow-hidden rounded-lg border border-gray-200 bg-gray-50 dark:border-gray-700 dark:bg-gray-800"
					>
						{#if h.kind === 'code'}
							<div class="flex h-full items-center justify-center text-xs text-gray-400">
								{h.info?.lines ? `lines ${h.info.lines}` : 'code'}
							</div>
						{:else if typeof thumbs[key] === 'string'}
							<img src={thumbs[key]} alt="preview" class="h-full w-full object-cover" loading="lazy" />
						{:else if thumbs[key] === null}
							<div class="flex h-full items-center justify-center">
								<Spinner />
							</div>
						{:else}
							<div class="flex h-full items-center justify-center text-xs text-gray-400">
								{h.kind}
							</div>
						{/if}
					</div>

					<div class="min-w-0 flex-1">
						<div class="truncate text-sm font-medium text-gray-900 dark:text-gray-100"
							title={h.path}>{h.path}</div>
						<div class="mt-0.5 text-xs text-gray-400 dark:text-gray-500">
							{h.kind}
							{#if h.loc != null} · at {h.loc}s{/if}
							{#if h.cosine != null}
								· <Tooltip content="cosine similarity of the meaning match">
									<span class="cursor-help">sim {h.cosine.toFixed(2)}</span>
								</Tooltip>
							{/if}
						</div>
						{#if h.kind === 'code' && expanded[codeKey]}
							<pre class="mt-2 overflow-x-auto rounded-lg bg-gray-50 p-2.5 text-[11px] leading-relaxed text-gray-700 dark:bg-gray-950/60 dark:text-gray-300"><code>{expanded[codeKey]}</code></pre>
						{/if}
						{#if h.kind !== 'code' && h.excerpt}
							<p class="mt-2 line-clamp-3 text-sm text-gray-600 dark:text-gray-400">{h.excerpt}</p>
						{/if}
					</div>
				</li>
			{/each}
		</ul>
	{:else if searched}
		<div class="mt-6 text-center text-sm text-gray-400 dark:text-gray-500">
			Nothing matched “{query}” in the indexed folders.
		</div>
	{/if}
</div>
