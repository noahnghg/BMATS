function Profile() {
    return (
        <div className="profile route">
            <div className="profileSection">
                <h2>Your Profile</h2>
                <div className="applicationMetricsWrapper">
                    <div className="applicationMetricLists">
                        <div className="applicationMetric">
                            <h3>Total Applications</h3>
                            <p>0</p>
                        </div>
                        <div className="applicationMetric">
                            <h3>Average Score</h3>
                            <p>--</p>
                        </div>
                        <div className="applicationMetric">
                            <h3>Best Match</h3>
                            <p>--</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Profile
