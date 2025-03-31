<script lang="ts">
	import { onMount } from 'svelte';
	import { writable, type Writable } from 'svelte/store';
	import dayjs from 'dayjs';

	interface Entry {
		id: string;
		timestamp: number;
		content: string;
	}

	const API_BASE_URL: string = 'http://localhost:5000/';
	const entries: Writable<Entry[]> = writable([]);
	const selectedRange: Writable<'day' | 'week'> = writable('day');
	const selectedDate: Writable<string> = writable(dayjs().format('YYYY-MM-DD'));

	export let weeklyEntries: Entry[] = [];

	async function fetchEntries() {
		const start = dayjs($selectedDate).startOf($selectedRange).unix();
		const end = dayjs($selectedDate).endOf($selectedRange).unix();
		
		try {
			const response = await fetch(`${API_BASE_URL}/entries?start=${start}&end=${end}`);
			const data: Entry[] = await response.json();
			console.log(data);
			entries.set(data);
			weeklyEntries = data;
		} catch (error) {
			console.error('Failed to fetch entries', error);
		}
	}

	async function deleteEntry(id: string) {
		try {
			const response = await fetch(`${API_BASE_URL}/delete/${id}`, { method: 'DELETE' });
			if (response.ok) {
				entries.update(e => e.filter(entry => entry.id !== id));
			}
		} catch (error) {
			console.error('Failed to delete entry', error);
		}
	}

	function copyToClipboard(content: string) {
		navigator.clipboard.writeText(content).then(() => {
			console.log('Copied to clipboard:', content);
		}).catch(err => {
			console.error('Failed to copy', err);
		});
	}

	onMount(fetchEntries);

	$: fetchEntries();
</script>

<style>
	td { padding: 12px 6px; }
</style>

<section class="bg-blue-500">
	<header class="py-6 text-center">
		<h2>Entries for the Week</h2>
	</header>

	<table>
		<tbody>
			{#each weeklyEntries as entry, index}
				<tr class="odd:bg-slate-200">
					<td>{index+1}</td>
					<td>
						{entry.timestamp}
					</td>
					<td>
						<pre class="text-wrap">{entry.content}</pre>
					</td>
					<td>
						<button on:click={() => copyToClipboard(entry.content)}>Copy</button>
					</td>
					<td>
						<button on:click={() => deleteEntry(entry.id)}>Delete</button>
					</td>
				</tr>
			{/each}
		</tbody>
	</table>
</section>
