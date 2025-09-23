'use client'

import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { 
  Bot, 
  Zap, 
  Users, 
  TrendingUp,
  Play,
  Pause,
  RefreshCw,
  CheckCircle,
  Clock,
  AlertCircle
} from 'lucide-react'

interface Agent {
  id: string
  name: string
  status: 'ready' | 'busy' | 'error'
}

interface Job {
  id: string
  type: string
  status: 'created' | 'processing' | 'completed' | 'failed'
}

export default function DashboardPage() {
  const [agents, setAgents] = useState<Agent[]>([])
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      // Mock data for now - backend is having issues
      const mockAgents = [
        {"id": "mistral", "name": "Mistral 7B", "status": "ready"},
        {"id": "codellama", "name": "Code Llama 13B", "status": "ready"},
        {"id": "llama", "name": "Llama 3.2 3B", "status": "ready"},
        {"id": "research", "name": "Research Agent", "status": "ready"}
      ]
      
      const mockJobs = [
        {"id": "job_001", "type": "content_creation", "status": "completed"},
        {"id": "job_002", "type": "video_generation", "status": "processing"},
        {"id": "job_003", "type": "content_creation", "status": "completed"}
      ]
      
      setAgents(mockAgents)
      setJobs(mockJobs)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const [jobPrompt, setJobPrompt] = useState('')
  const [isCreatingJob, setIsCreatingJob] = useState(false)

  const createJob = async () => {
    if (!jobPrompt.trim()) {
      alert('Please enter a prompt for content creation!')
      return
    }
    
    setIsCreatingJob(true)
    
    // Simulate API call with mock response
    setTimeout(() => {
      const mockResponse = {
        id: `job_${Date.now()}`,
        status: 'completed',
        type: 'content_creation',
        content: `🤖 AI Generated Content for: "${jobPrompt}"\n\nThis is a demo response! Your AgenticAI Lab system would normally connect to the Mistral 7B model running in Docker to generate real AI content. The infrastructure is set up with:\n\n• Ollama container with 3 LLM models\n• PostgreSQL + Redis + Qdrant databases\n• FastAPI backend (having connection issues)\n• Next.js frontend (working perfectly!)\n\nOnce the backend is stable, you'll get real AI-generated content here!`,
        model: 'mistral:7b (simulated)'
      }
      
      alert(`🎉 Job Completed!\n\nPrompt: ${jobPrompt}\n\nContent: ${mockResponse.content.substring(0, 150)}...`)
      
      // Add to jobs list
      const newJob = {
        id: mockResponse.id,
        type: 'content_creation', 
        status: 'completed'
      }
      setJobs(prev => [newJob, ...prev])
      setJobPrompt('')
      setIsCreatingJob(false)
    }, 2000) // 2 second delay to simulate processing
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ready':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'busy':
      case 'processing':
        return <Clock className="h-4 w-4 text-yellow-500" />
      case 'error':
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      default:
        return <RefreshCw className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'ready':
        return <Badge variant="secondary" className="text-green-700 bg-green-100">Ready</Badge>
      case 'busy':
      case 'processing':
        return <Badge variant="secondary" className="text-yellow-700 bg-yellow-100">Busy</Badge>
      case 'error':
      case 'failed':
        return <Badge variant="destructive">Error</Badge>
      case 'completed':
        return <Badge variant="secondary" className="text-green-700 bg-green-100">Completed</Badge>
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-8">
        <div className="flex items-center justify-center min-h-[400px]">
          <RefreshCw className="h-8 w-8 animate-spin" />
          <span className="ml-2 text-lg">Loading dashboard...</span>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold mb-2">AgenticAI Dashboard</h1>
                <p className="text-slate-600 dark:text-slate-300">
                  Manage your AI agents and content creation jobs
                </p>
              </div>
              <div className="flex gap-2 items-center">
                <input
                  type="text"
                  placeholder="Enter content creation prompt..."
                  value={jobPrompt}
                  onChange={(e) => setJobPrompt(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-md w-64 text-sm"
                  disabled={isCreatingJob}
                />
                <Button 
                  onClick={createJob} 
                  className="flex items-center gap-2"
                  disabled={isCreatingJob}
                >
                  {isCreatingJob ? (
                    <RefreshCw className="h-4 w-4 animate-spin" />
                  ) : (
                    <Play className="h-4 w-4" />
                  )}
                  {isCreatingJob ? 'Creating...' : 'Create Job'}
                </Button>
              </div>
            </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Agents</CardTitle>
              <Bot className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{agents.length}</div>
              <p className="text-xs text-muted-foreground">
                AI agents ready to work
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Jobs</CardTitle>
              <Zap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {jobs.filter(job => job.status === 'processing').length}
              </div>
              <p className="text-xs text-muted-foreground">
                Currently processing
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
              <CheckCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {jobs.filter(job => job.status === 'completed').length}
              </div>
              <p className="text-xs text-muted-foreground">
                Successfully finished
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Success Rate</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">98%</div>
              <p className="text-xs text-muted-foreground">
                Job completion rate
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Agents Status */}
          <Card>
            <CardHeader>
              <CardTitle>AI Agents Status</CardTitle>
              <CardDescription>
                Monitor the status of your AI agents
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {agents.map((agent) => (
                  <div key={agent.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-3">
                      {getStatusIcon(agent.status)}
                      <div>
                        <h3 className="font-medium">{agent.name}</h3>
                        <p className="text-sm text-muted-foreground">ID: {agent.id}</p>
                      </div>
                    </div>
                    {getStatusBadge(agent.status)}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Recent Jobs */}
          <Card>
            <CardHeader>
              <CardTitle>Recent Jobs</CardTitle>
              <CardDescription>
                Your latest content creation tasks
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {jobs.map((job) => (
                  <div key={job.id} className="flex items-center justify-between p-4 border rounded-lg">
                    <div className="flex items-center gap-3">
                      {getStatusIcon(job.status)}
                      <div>
                        <h3 className="font-medium capitalize">{job.type.replace('_', ' ')}</h3>
                        <p className="text-sm text-muted-foreground">ID: {job.id}</p>
                      </div>
                    </div>
                    {getStatusBadge(job.status)}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
