import { useState, useEffect } from 'react'

function Jobs() {
    const [jobs, setJobs] = useState([])
    const [searchQuery, setSearchQuery] = useState('')

    useEffect(() => {
        fetchJobs()
    }, [])

    const fetchJobs = async () => {
        try {
            const response = await fetch('/api/jobs/')
            const data = await response.json()
            setJobs(data)
        } catch (error) {
            console.error('Error fetching jobs:', error)
        }
    }

    const filteredJobs = jobs.filter(job =>
        job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.company.toLowerCase().includes(searchQuery.toLowerCase())
    )

    return (
        <div className="jobs route">
            <form className="searchForm" onSubmit={(e) => e.preventDefault()}>
                <input
                    type="search"
                    placeholder="Search a job..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </form>
            <div className="joblistingsWrapper">
                <div className="joblistings">
                    {filteredJobs.map((job) => (
                        <div key={job.id} className="jobcard">
                            <div className="cardHeader">
                                <div className="jobTitle">{job.title}</div>
                                <div className="organization">{job.company}</div>
                            </div>
                            <div className="cardBody">
                                <div className="jobDesc">{job.description}</div>
                                <div className="requirements">{job.requirements}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

export default Jobs
