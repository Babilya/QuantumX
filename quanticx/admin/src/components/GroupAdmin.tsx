import React, { useState } from 'react'

export default function GroupAdmin(){
  const [groupId, setGroupId] = useState('')
  const [welcome, setWelcome] = useState('')
  const [caps, setCaps] = useState(true)
  const [premium, setPremium] = useState(false)

  async function save(){
    const body = { group_id: groupId, welcome_text: welcome, caps_filter: caps?1:0, premium_enabled: premium?1:0 }
    await fetch('/api/groups/set', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body) })
    alert('Saved')
  }

  return (
    <div className="panel">
      <label>Group ID <input value={groupId} onChange={e=>setGroupId(e.target.value)} placeholder="-100..." /></label>
      <label>Welcome <input value={welcome} onChange={e=>setWelcome(e.target.value)} /></label>
      <label><input type="checkbox" checked={caps} onChange={e=>setCaps(e.target.checked)} /> Caps filter</label>
      <label><input type="checkbox" checked={premium} onChange={e=>setPremium(e.target.checked)} /> Premium enabled</label>
      <button onClick={save}>Save</button>
    </div>
  )
}
