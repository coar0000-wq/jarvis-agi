import React, { useState, useEffect } from 'react'
import './App.css'

export default function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/dashboard-data.json')
        const json = await response.json()
        setData(json)
      } catch (error) {
        console.error('Error loading data:', error)
      }
      setLoading(false)
    }

    fetchData()
    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return <div className="loading">대시보드 로딩 중...</div>
  }

  if (!data) {
    return <div className="error">데이터를 불러올 수 없습니다</div>
  }

  return (
    <div className="dashboard">
      {/* 헤더 */}
      <header className="header">
        <h1>🤖 JARVIS 통합 대시보드</h1>
        <div className="header-stats">
          <div className="stat">
            <span className="label">전체 진행도</span>
            <span className="value">{data.stats.totalProgress}%</span>
          </div>
          <div className="stat">
            <span className="label">팀원 온라인</span>
            <span className="value">{data.stats.teamOnline}/6</span>
          </div>
          <div className="stat">
            <span className="label">시스템 상태</span>
            <span className="value">✅ {data.stats.systemsHealthy}/4</span>
          </div>
        </div>
      </header>

      {/* 프로젝트 카드 */}
      <section className="projects">
        <h2>📊 프로젝트 진행도</h2>
        <div className="cards">
          {/* DAISO */}
          <div className="card" style={{ borderColor: data.projects.daiso.color }}>
            <div className="card-header">
              <h3>{data.projects.daiso.title}</h3>
              <span className="status">{data.projects.daiso.status}</span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${data.projects.daiso.progress}%`,
                  backgroundColor: data.projects.daiso.color
                }}
              />
            </div>
            <div className="progress-text">{data.projects.daiso.progress}%</div>
            <div className="metrics">
              {Object.entries(data.projects.daiso.metrics).map(([key, value]) => (
                <div key={key} className="metric">
                  <span className="metric-label">{key}:</span>
                  <span className="metric-value">{value}</span>
                </div>
              ))}
            </div>
            <div className="last-update">마지막 업데이트: {data.projects.daiso.lastUpdate}</div>
          </div>

          {/* JARVIS */}
          <div className="card" style={{ borderColor: data.projects.jarvis.color }}>
            <div className="card-header">
              <h3>{data.projects.jarvis.title}</h3>
              <span className="badge">{data.projects.jarvis.metrics.phase}</span>
            </div>
            <div className="metrics">
              {Object.entries(data.projects.jarvis.metrics).map(([key, value]) => (
                <div key={key} className="metric">
                  <span className="metric-label">{key}:</span>
                  <span className="metric-value">{value}</span>
                </div>
              ))}
            </div>
            <div className="last-update">마지막 업데이트: {data.projects.jarvis.lastUpdate}</div>
          </div>

          {/* 채용 */}
          <div className="card" style={{ borderColor: data.projects.recruitment.color }}>
            <div className="card-header">
              <h3>{data.projects.recruitment.title}</h3>
              <span className="status">{data.projects.recruitment.metrics.current}</span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${(data.projects.recruitment.current / data.projects.recruitment.target) * 100}%`,
                  backgroundColor: data.projects.recruitment.color
                }}
              />
            </div>
            <div className="progress-text">{data.projects.recruitment.metrics.target_pct}</div>
            <div className="metrics">
              {Object.entries(data.projects.recruitment.metrics).map(([key, value]) => (
                <div key={key} className="metric">
                  <span className="metric-label">{key}:</span>
                  <span className="metric-value">{value}</span>
                </div>
              ))}
            </div>
            <div className="last-update">마지막 업데이트: {data.projects.recruitment.lastUpdate}</div>
          </div>
        </div>
      </section>

      {/* 팀원 상태 */}
      <section className="team">
        <h2>👥 팀원 상태 (6명)</h2>
        <div className="team-grid">
          {data.team.map((member) => (
            <div key={member.id} className="team-card">
              <div className="avatar">{member.avatar}</div>
              <div className="team-info">
                <h4>{member.name}</h4>
                <p className="role">{member.role}</p>
                <p className="task">작업: {member.task}</p>
                <div className="team-progress">
                  <div className="progress-bar small">
                    <div
                      className="progress-fill"
                      style={{ width: `${member.progress}%` }}
                    />
                  </div>
                  <span className="progress-text">{member.progress}%</span>
                </div>
                <p className="status">
                  <span className={`status-badge ${member.status}`}>
                    {member.status === 'active' ? '🟢 활동 중' : '⚪ 대기'}
                  </span>
                </p>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 시스템 상태 */}
      <section className="systems">
        <h2>⚙️ 시스템 상태</h2>
        <div className="systems-grid">
          {Object.entries(data.systems).map(([key, system]) => (
            <div key={key} className="system-card">
              <div className="system-header">
                <h4>{system.name}</h4>
                <span className={`status-indicator ${system.status}`}>
                  {system.status === 'online' ? '🟢 온라인' : '🔴 오프라인'}
                </span>
              </div>
              <p className="detail">{system.detail}</p>
              <p className="last-check">마지막 확인: {system.lastCheck || system.lastRun || system.lastSync}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 최근 업데이트 */}
      <section className="updates">
        <h2>📋 최근 업데이트</h2>
        <div className="update-list">
          {data.updates.map((update, idx) => (
            <div key={idx} className="update-item">
              <span className="time">{update.time}</span>
              <span className={`type ${update.type}`}>
                {update.type === 'success' ? '✅' : '⚠️'}
              </span>
              <span className="message">{update.message}</span>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
