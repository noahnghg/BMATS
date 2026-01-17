function Sidebar({ onNavigate }) {
    const navItems = ['Jobs', 'Profile', 'Applications']

    return (
        <aside>
            <div className="profilebanner">
                <div className="bannerWrapper">
                    <div className="userProfilePic">
                        <i className="fa-solid fa-user"></i>
                    </div>
                    <div className="userName">John Doe</div>
                </div>
            </div>
            <nav className="menuNav">
                <ul className="mainNav">
                    {navItems.map((item, idx) => (
                        <li
                            key={item}
                            className="navItem"
                            onClick={() => onNavigate(idx)}
                        >
                            {item}
                        </li>
                    ))}
                </ul>
                <div className="logOutBtn">Log out</div>
            </nav>
        </aside>
    )
}

export default Sidebar
