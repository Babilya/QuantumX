<script>
  let groupId = ''
  let welcome = ''
  let caps = true
  let premium = false

  async function save() {
    const body = { group_id: groupId, welcome_text: welcome, caps_filter: caps?1:0, premium_enabled: premium?1:0 }
    await fetch('/api/groups/set', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
    alert('Saved')
  }
</script>

<div class="panel">
  <label>Group ID <input bind:value={groupId} placeholder="-100..." /></label>
  <label>Welcome <input bind:value={welcome} /></label>
  <label><input type="checkbox" bind:checked={caps} /> Caps filter</label>
  <label><input type="checkbox" bind:checked={premium} /> Premium enabled</label>
  <button on:click={save}>Save</button>
</div>

<style>
.panel { display:grid; gap:12px; max-width:520px }
label { color:white; display:grid; gap:6px }
input { padding:8px 10px; border-radius:8px; border:1px solid #333; background:#151518; color:#fff }
button{ background:linear-gradient(90deg,#FF1CC0,#1C3AFF); color:#fff; border:none; padding:10px 14px; border-radius:10px }
</style>
