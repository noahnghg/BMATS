import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import Jobs from './components/Jobs'
import Profile from './components/Profile'
import Applications from './components/Applications'
import './index.css'

function App() {
    const [activeRoute, setActiveRoute] = useState(0)
    const [currentUser, setCurrentUser] = useState(null)

    useEffect(() => {
        // Check if user exists (for demo, using test-user-001)
        checkUser()
    }, [])

    const checkUser = async () => {
        try {
            const response = await fetch('/api/users/test-user-001')
            if (response.ok) {
                const data = await response.json()
                setCurrentUser(data)
            }
        } catch (error) {
            console.log('No existing user found')
        }
    }

    return (
        <>
            <main>
                <Sidebar onNavigate={setActiveRoute} activeIndex={activeRoute} />
                <div className="mainContentWrapper">
                    <div
                        className="routes"
                        style={{ transform: `translateX(-${activeRoute * (100 / 3)}%)` }}
                    >
                        <Jobs currentUser={currentUser} />
                        <Profile currentUser={currentUser} setCurrentUser={setCurrentUser} />
                        <Applications currentUser={currentUser} />
                    </div>
                </div>
            </main>
        </>
    )
}

export default App
