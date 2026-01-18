function Sidebar({ onNavigate, activeIndex }) {
    const navItems = [
        { name: 'Jobs', icon: 'fa-briefcase' },
        { name: 'Profile', icon: 'fa-user' },
        { name: 'Applications', icon: 'fa-file-lines' }
    ]

    return (
        <aside>
            <nav className="menuNav">
                <ul className="mainNav">
                    {navItems.map((item, idx) => (
                        <li
                            key={item.name}
                            className={`navItem ${activeIndex === idx ? 'active' : ''}`}
                            onClick={() => onNavigate(idx)}
                        >
                            <i className={`fa-solid ${item.icon}`}></i>
                            {item.name}
                        </li>
                    ))}
                </ul>

                <div className="sidebarBottom">
                    <div className="profilebanner">
                        <div className="bannerWrapper">
                            <div className="userProfilePic">
                                <i className="fa-solid fa-user"></i>
                            </div>
                            <div className="userName">John Doe</div>
                        </div>
                    </div>
                    <div className="logOutBtn">
                        <i className="fa-solid fa-right-from-bracket"></i> Log out
                    </div>
                </div>
            </nav>
        </aside>
    )
}

export default Sidebar
