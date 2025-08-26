import React from 'react'

const tabs = [
  { key: 'home', label: 'Home' },
  { key: 'wallet', label: 'Wallet' },
  { key: 'shop', label: 'Shop' },
  { key: 'games', label: 'Games' },
  { key: 'osint', label: 'OSINT' },
]

export function BottomNav({ active, onChange }: { active: string; onChange: (k: string) => void }) {
  return (
    <nav className="bottom">
      {tabs.map(t => (
        <button key={t.key} className={active === t.key ? 'active' : ''} onClick={() => onChange(t.key)}>{t.label}</button>
      ))}
    </nav>
  )
}
