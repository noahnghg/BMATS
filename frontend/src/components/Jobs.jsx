import { useState, useEffect } from 'react'
import { createPortal } from 'react-dom'

function Jobs({ currentUser }) {
    const [jobs, setJobs] = useState([])
    const [searchQuery, setSearchQuery] = useState('')
    const [loading, setLoading] = useState(true)
    const [selectedJob, setSelectedJob] = useState(null)
    const [showPopup, setShowPopup] = useState(false)

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
        } finally {
            setLoading(false)
        }
    }

    const filteredJobs = jobs.filter(job =>
        job.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.company.toLowerCase().includes(searchQuery.toLowerCase()) ||
        job.description.toLowerCase().includes(searchQuery.toLowerCase())
    )

    const handleJobClick = (job) => {
        setSelectedJob(job)
        setShowPopup(true)
    }

    const handleClosePopup = () => {
        setShowPopup(false)
        setSelectedJob(null)
    }

    const handleFileUpload = async (e) => {
        const file = e.target.files[0]
        if (!file || !selectedJob) return

        const formData = new FormData()
        formData.append('file', file)
        formData.append('user_id', currentUser?.id || 'new-user')

        try {
            const uploadRes = await fetch('/api/users/upload-resume', {
                method: 'POST',
                body: formData
            })
            const userData = await uploadRes.json()

            const appRes = await fetch('/api/applications/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: userData.user_id,
                    jobId: selectedJob.id
                })
            })
            const appData = await appRes.json()

            alert(`Application submitted! Score: ${(appData.score * 100).toFixed(1)}%`)
            handleClosePopup()
        } catch (error) {
            console.error('Error applying:', error)
            alert('Failed to submit application')
        }
    }

    const handleUseExisting = async () => {
        if (!currentUser || !selectedJob) return

        try {
            const response = await fetch('/api/applications/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userId: currentUser.id,
                    jobId: selectedJob.id
                })
            })
            const data = await response.json()
            alert(`Application submitted! Score: ${(data.score * 100).toFixed(1)}%`)
            handleClosePopup()
        } catch (error) {
            console.error('Error applying:', error)
            alert('Failed to submit application')
        }
    }

    // Popup rendered via Portal to escape parent overflow/transform
    const popup = showPopup && selectedJob && createPortal(
        <div className="popupWrapper active" onClick={handleClosePopup}>
            <div className="popContent" onClick={(e) => e.stopPropagation()}>
                <button className="popupClose" onClick={handleClosePopup}>
                    <i className="fa-solid fa-xmark"></i>
                </button>

                <div className="popupHeader">
                    <h2 className="popupTitle">{selectedJob.title}</h2>
                    <p className="popupCompany">{selectedJob.company}</p>
                </div>

                <div className="popupBody">
                    <div className="jobFullDesc">
                        <h3>Description</h3>
                        <p>{selectedJob.description}</p>
                    </div>

                    <div className="jobRequirements">
                        <h3>Requirements</h3>
                        <p>{selectedJob.requirements}</p>
                    </div>
                </div>

                <div className="popupActions">
                    {currentUser && currentUser.skills && (
                        <div className="useExistingSection">
                            <h3>Use Existing Resume</h3>
                            <div className="existingResumeBox" onClick={handleUseExisting}>
                                <i className="fa-solid fa-file-lines"></i>
                                <span>Apply with your saved profile</span>
                            </div>
                        </div>
                    )}

                    <div className="uploadNewSection">
                        <h3>Upload Your Resume</h3>
                        <label className="uploadDropArea">
                            <input
                                type="file"
                                accept=".pdf"
                                style={{ display: 'none' }}
                                onChange={handleFileUpload}
                            />
                            <i className="fa-solid fa-cloud-arrow-up"></i>
                            <span>Drop your resume here or click to browse</span>
                            <small>PDF files only</small>
                        </label>
                    </div>
                </div>
            </div>
        </div>,
        document.body
    )

    return (
        <div className="jobs route">
            <div className="pageHeader">
                <h1 className="pageTitle">Find Your Next Role</h1>
                <p className="pageSubtitle">Browse open positions and apply with your profile</p>
            </div>

            <form className="searchForm" onSubmit={(e) => e.preventDefault()}>
                <input
                    type="search"
                    placeholder="Search jobs by title, company, or keywords..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                />
            </form>

            <div className="joblistingsWrapper">
                {loading ? (
                    <div className="emptyState">
                        <p>Loading jobs...</p>
                    </div>
                ) : filteredJobs.length === 0 ? (
                    <div className="emptyState">
                        <i className="fa-solid fa-briefcase"></i>
                        <h3>No jobs found</h3>
                        <p>Try adjusting your search criteria</p>
                    </div>
                ) : (
                    <div className="joblistings">
                        {filteredJobs.map((job) => (
                            <div
                                key={job.id}
                                className="jobcard"
                                onClick={() => handleJobClick(job)}
                            >
                                <div className="cardHeader">
                                    <div className="jobTitle">{job.title}</div>
                                    <div className="organization">{job.company}</div>
                                </div>
                                <div className="cardBody">
                                    <div className="jobDesc">{job.description}</div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {popup}
        </div>
    )
}

export default Jobs
