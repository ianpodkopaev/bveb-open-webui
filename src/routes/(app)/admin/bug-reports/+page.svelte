<script lang="ts">
	import { onMount, getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { getBugReports } from '$lib/apis/bug-reports';

	const i18n = getContext('i18n');

	let reports = [];
	let loading = true;
	let expandedId: string | null = null;

	const toggleExpand = (id: string) => {
		expandedId = expandedId === id ? null : id;
	};

	const formatDateTime = (timestamp: number) => {
		const d = new Date(timestamp * 1000);
		return d.toLocaleString('ru-RU', {
			year: 'numeric',
			month: '2-digit',
			day: '2-digit',
			hour: '2-digit',
			minute: '2-digit',
			second: '2-digit'
		});
	};

	onMount(async () => {
		try {
			reports = await getBugReports(localStorage.token);
		} catch (err) {
			toast.error($i18n.t('Failed to load reports'));
		} finally {
			loading = false;
		}
	});
</script>

<div class="p-4 max-w-5xl mx-auto">
	<div class="text-xl font-medium mb-4 dark:text-gray-100">
		{$i18n.t('Bug Reports & Feedback')}
		<span class="text-sm text-gray-500 font-normal ml-2">({reports.length})</span>
	</div>

	{#if loading}
		<div class="text-center text-gray-500 py-8">{$i18n.t('Loading...')}</div>
	{:else if reports.length === 0}
		<div class="text-center text-gray-500 py-8">{$i18n.t('No reports yet')}</div>
	{:else}
		<div class="overflow-x-auto">
			<table class="w-full text-sm">
				<thead>
					<tr class="border-b border-gray-200 dark:border-gray-700 text-left text-gray-500 dark:text-gray-400">
						<th class="py-2 pr-4 w-8"></th>
						<th class="py-2 pr-4">{$i18n.t('Date')}</th>
						<th class="py-2 pr-4">{$i18n.t('Name')}</th>
						<th class="py-2 pr-4">{$i18n.t('Email')}</th>
						<th class="py-2 pr-4">{$i18n.t('Category')}</th>
						<th class="py-2">{$i18n.t('Message')}</th>
					</tr>
				</thead>
				<tbody>
					{#each reports as report}
						{@const isExpanded = expandedId === report.id}
						<tr
							class="border-b border-gray-100 dark:border-gray-800 cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
							on:click={() => toggleExpand(report.id)}
						>
							<td class="py-2 pr-2 text-gray-400">
								<svg
									class="w-4 h-4 transition-transform {isExpanded ? 'rotate-90' : ''}"
									viewBox="0 0 20 20"
									fill="currentColor"
								>
									<path fill-rule="evenodd" d="M7.21 14.77a.75.75 0 01.02-1.06L11.168 10 7.23 6.29a.75.75 0 111.04-1.08l4.5 4.25a.75.75 0 010 1.08l-4.5 4.25a.75.75 0 01-1.06-.02z" clip-rule="evenodd" />
								</svg>
							</td>
							<td class="py-2 pr-4 text-xs text-gray-400 whitespace-nowrap">
								{formatDateTime(report.created_at)}
							</td>
							<td class="py-2 pr-4 dark:text-gray-200">{report.data?.name ?? '-'}</td>
							<td class="py-2 pr-4 dark:text-gray-200">{report.data?.email ?? '-'}</td>
							<td class="py-2 pr-4">
								<span
									class="inline-block px-2 py-0.5 rounded-full text-xs font-medium {report.data?.category === 'Пожаловаться на баг'
										? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
										: report.data?.category === 'UI/UX отзыв'
											? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400'
											: 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400'}"
								>
									{report.data?.category ?? '-'}
								</span>
							</td>
							<td class="py-2 max-w-xs">
								<div class="truncate dark:text-gray-300" title={report.data?.message}>
									{report.data?.message ?? '-'}
								</div>
							</td>
						</tr>

						{#if isExpanded}
							<tr class="border-b border-gray-100 dark:border-gray-800">
								<td colspan="6" class="px-6 py-4 bg-gray-50 dark:bg-gray-800/30">
									<div class="flex flex-col gap-3 max-w-3xl">
										<div>
											<span class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{$i18n.t('Message')}</span>
											<p class="mt-1 text-sm dark:text-gray-200 whitespace-pre-wrap">{report.data?.message ?? '-'}</p>
										</div>

										{#if report.data?.bug_time}
											<div>
												<span class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{$i18n.t('Время бага')}</span>
												<p class="mt-1 text-sm dark:text-gray-200">{report.data.bug_time}</p>
											</div>
										{/if}

										{#if report.data?.photo}
											<div>
												<span class="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">{$i18n.t('Фото')}</span>
												<div class="mt-1">
													<img
														src={report.data.photo}
														alt="bug screenshot"
														class="max-h-64 rounded-lg border border-gray-200 dark:border-gray-700 object-contain"
													/>
												</div>
											</div>
										{/if}
									</div>
								</td>
							</tr>
						{/if}
					{/each}
				</tbody>
			</table>
		</div>
	{/if}
</div>
