<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { onMount, getContext } from 'svelte';

	import Modal from '$lib/components/common/Modal.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';
	import { searchKnowledgeBases } from '$lib/apis/knowledge';
	import { addNoteToKnowledgeById, updateNoteInKnowledgeById } from '$lib/apis/knowledge';

	const i18n = getContext('i18n');

	export let show = false;
	export let noteId = '';

	let kbs: any[] = [];
	let selectedKbId: string = '';
	let loading = false;
	let searching = false;

	let duplicateInfo: { fileId: string; noteId: string; kbId: string } | null = null;
	let showConfirmDialog = false;

	const loadKnowledgeBases = async () => {
		searching = true;
		try {
			const res = await searchKnowledgeBases(localStorage.token);
			kbs = (Array.isArray(res) ? res : res?.items ?? res?.data ?? [])
				.filter((kb: any) => kb?.write_access === true)
				.map((kb: any) => ({
					id: kb.id,
					name: kb.name,
					description: kb.description ?? '',
					file_count: kb.data?.file_ids?.length ?? 0
				}));
		} catch {
			kbs = [];
		}
		searching = false;
	};

	$: if (show) {
		selectedKbId = '';
		duplicateInfo = null;
		showConfirmDialog = false;
		loadKnowledgeBases();
	};

	const submitHandler = async () => {
		if (!selectedKbId) {
			toast.error($i18n.t('Выберите базу знаний'));
			return;
		}

		loading = true;
		try {
			const res = await addNoteToKnowledgeById(localStorage.token, selectedKbId, noteId);

			if (res?.duplicate) {
				duplicateInfo = {
					fileId: res.existing_file_id,
					noteId: res.note_id,
					kbId: selectedKbId
				};
				showConfirmDialog = true;
				loading = false;
				return;
			}

			toast.success($i18n.t('Заметка опубликована в базу знаний'));
			show = false;
		} catch (e: any) {
			toast.error(typeof e === 'string' ? e : $i18n.t('Ошибка при публикации'));
		}
		loading = false;
	};

	const confirmUpdate = async () => {
		if (!duplicateInfo) return;

		loading = true;
		try {
			await updateNoteInKnowledgeById(
				localStorage.token,
				duplicateInfo.kbId,
				duplicateInfo.noteId,
				duplicateInfo.fileId
			);
			toast.success($i18n.t('Заметка обновлена в базе знаний'));
			show = false;
		} catch (e: any) {
			toast.error(typeof e === 'string' ? e : $i18n.t('Ошибка при обновлении'));
		}
		loading = false;
	};
</script>

<Modal size="sm" bind:show>
	<div>
		<div class="flex justify-between dark:text-gray-100 p-4 pb-0">
			<div class="text-lg font-semibold">
				{showConfirmDialog ? $i18n.t('Заметка уже в базе') : $i18n.t('Опубликовать в базу знаний')}
			</div>
			<button
				class="self-center"
				on:click={() => {
					show = false;
				}}
			>
				<XMark className="size-5" />
			</button>
		</div>

		{#if showConfirmDialog}
			<div class="p-4">
				<div class="p-3 bg-amber-50 dark:bg-amber-900/20 rounded-xl border border-amber-200 dark:border-amber-800">
					<div class="text-sm font-medium text-amber-800 dark:text-amber-200">
						{$i18n.t('Эта заметка уже добавлена в базу знаний')}
					</div>
					<div class="text-xs text-amber-600 dark:text-amber-400 mt-1">
						{$i18n.t('Обновить содержимое существующей записи?')}
					</div>
				</div>

				<div class="flex justify-end gap-2 mt-4">
					<button
						class="px-3.5 py-2 bg-white dark:bg-gray-900 dark:text-gray-300 rounded-full text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-800 border border-gray-100 dark:border-gray-800"
						on:click={() => {
							showConfirmDialog = false;
							duplicateInfo = null;
						}}
					>
						{$i18n.t('Отмена')}
					</button>
					<button
						class="px-3.5 py-2 bg-black text-white dark:bg-white dark:text-black rounded-full text-sm font-medium transition {loading
							? 'opacity-50 pointer-events-none'
							: ''}"
						on:click={confirmUpdate}
					>
						{loading ? $i18n.t('Обновление...') : $i18n.t('Обновить')}
					</button>
				</div>
			</div>
		{:else}
			<div class="p-4 flex flex-col gap-2">
				<div class="text-sm text-gray-500 dark:text-gray-400">
					{$i18n.t('Выберите базу знаний для публикации этой заметки')}
				</div>

				{#if searching}
					<div class="flex justify-center py-6">
						<div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-gray-400" />
					</div>
				{:else if kbs.length === 0}
					<div class="text-center py-6 text-gray-500 text-sm">
						{$i18n.t('Нет доступных баз знаний для записи')}
					</div>
				{:else}
					<div class="flex flex-col gap-1 max-h-[300px] overflow-y-auto">
						{#each kbs as kb}
							<button
								class="text-left p-3 rounded-xl text-sm border transition
								{selectedKbId === kb.id
								? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20 dark:border-blue-400'
								: 'border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800'}"
								on:click={() => {
									selectedKbId = kb.id;
								}}
							>
								<div class="font-medium truncate">{kb.name}</div>
								{#if kb.description}
									<div class="text-gray-500 dark:text-gray-400 text-xs mt-0.5 line-clamp-1">
										{kb.description}
									</div>
								{/if}
							</button>
						{/each}
					</div>
				{/if}
			</div>

			<div class="flex justify-end p-4 pt-0 gap-2">
				<button
					class="px-3.5 py-2 bg-white dark:bg-gray-900 dark:text-gray-300 rounded-full text-sm font-medium transition hover:bg-gray-50 dark:hover:bg-gray-800 border border-gray-100 dark:border-gray-800"
					on:click={() => {
						show = false;
					}}
				>
					{$i18n.t('Отмена')}
				</button>
				<button
					class="px-3.5 py-2 bg-black text-white dark:bg-white dark:text-black rounded-full text-sm font-medium transition {loading || !selectedKbId
						? 'opacity-50 pointer-events-none'
						: ''}"
					on:click={submitHandler}
				>
					{loading ? $i18n.t('Публикация...') : $i18n.t('Опубликовать')}
				</button>
			</div>
		{/if}
	</div>
</Modal>
