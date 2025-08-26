<script>
  const tabs = [
    'Dashboard','User Management','Payments Logs','Currency Audit','AI Usage',
    'OSINT Reports','Shop Inventory','Affiliate Stats','Bonus Tracker','Analytics',
    'Dating','Casino','Guarantor','Groups','CRM','Streaming','NFT Creator','Events',
    'Fitness','Language Tutor','Crypto Simulator','Ads Platform','Subscriptions',
    'VR/AR','Crypto Farm','Social','E-Learning','Health','Music','Travel','Jobs',
    'Pet Care','Eco Tracker','Valuation','Content Gen','Premium Chats'
  ]
  let active = tabs[0]
  import GroupAdmin from './components/GroupAdmin.svelte'
</script>

<div class="layout">
  <aside>
    {#each tabs as t}
      <div class:active={t===active} on:click={() => active=t}>{t}</div>
    {/each}
  </aside>
  <section>
    <h2>{active}</h2>
    {#if active === 'Groups'}
      <GroupAdmin />
    {:else}
      <p>Placeholder panel</p>
    {/if}
  </section>
</div>

<style>
.layout{ display:grid; grid-template-columns: 240px 1fr; height:100vh; }
body{ margin:0; background:#0E0E10; font-family:Inter,system-ui,sans-serif }
aside{ background:#0E0E10; padding:12px; border-right:1px solid #222; color:#fff }
aside div{ padding:8px 10px; cursor:pointer; border-radius:8px; }
aside div.active{ background: linear-gradient(90deg,#FF1CC0,#1C3AFF); color:#fff }
section{ padding:20px; color:white }
</style>
