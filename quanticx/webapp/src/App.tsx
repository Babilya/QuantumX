import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useTheme } from './store'
import { BottomNav } from './components/BottomNav'

export default function App() {
  const { t } = useTranslation()
  const { theme, toggle } = useTheme()
  const [tab, setTab] = useState('home')

  return (
    <div data-theme={theme} className="app">
      <header>
        <h1>{t('title')}</h1>
        <button onClick={toggle}>Theme</button>
      </header>
      <main>
        {tab === 'home' && <p>{t('welcome')}</p>}
        {tab === 'wallet' && <p>Wallet</p>}
        {tab === 'shop' && <p>Shop</p>}
        {tab === 'games' && <p>Games</p>}
        {tab === 'osint' && <p>OSINT</p>}
      </main>
      <BottomNav active={tab} onChange={setTab} />
    </div>
  )
}
