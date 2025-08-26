import React, { useState } from 'react'
import GroupAdmin from './components/GroupAdmin'

const TABS = [
  'Dashboard','User Management','Module Control','AI Services','Economy System',
  'OSINT Tools','Dating Engine','Escrow','Casino Games','Shop Integration',
  'Telegram Bot','WebSocket Server','Security System','Real-time Monitoring','Optimization Engine',
  'Integrations','Configuration','System Monitoring','Logs Management','Analytics','Emergency Controls'
]

export default function App(){
  const [active, setActive] = useState(TABS[0])
  return (
    <div className="layout">
      <aside>
        {TABS.map(t => (
          <div key={t} className={active===t? 'active':''} onClick={()=>setActive(t)}>{t}</div>
        ))}
      </aside>
      <section>
        <h2>{active}</h2>
        {active === 'Groups' ? <GroupAdmin /> : <p>Placeholder</p>}
      </section>
    </div>
  )
}
