import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Jobs from './components/Jobs'
import Profile from './components/Profile'
import Applications from './components/Applications'
import './index.css'

function App() {
    const [activeRoute, setActiveRoute] = useState(0)

    return (
        <main>
            <Sidebar onNavigate={setActiveRoute} />
            <div className="mainContentWrapper">
                <div
                    className="routes"
                    style={{ transform: `translateX(-${activeRoute * (100 / 3)}%)` }}
                >
                    <Jobs />
                    <Profile />
                    <Applications />
                </div>
            </div>
        </main>
    )
}

export default App
