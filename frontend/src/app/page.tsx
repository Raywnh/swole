"use client"

import { useState } from "react"
import { ChangeEvent } from "react"
import axios from "axios"
import { ClipLoader } from 'react-spinners'

export default function Home() {
  const [image, setImage] = useState<string>("")
  const [uploadFile, setUploadFile] = useState<File | null>(null)
  const [loading, setLoading] = useState<boolean>(false)

  const handleImageChange = (e: ChangeEvent<HTMLInputElement>): void => {
      const file: File | null = e.target.files ? e.target.files[0] : null
      
      if (file) {
        setImage(URL.createObjectURL(file))
        setUploadFile(file)
      }
  }

  const uploadImage = async (): Promise<void> => {
    if (uploadFile) {
      setLoading(true)

      const formData = new FormData()
      formData.append("file", uploadFile)

      try {
        const res = await axios.post("http://127.0.0.1:8000/enlarged", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          },
          responseType: 'blob'
        })

        const image: Blob = res.data
        setImage(URL.createObjectURL(image))

      } catch (error) {
        console.error("Server Error: ", error)
      }
      setLoading(false)
    }
  }

  return (
      <div className="flex-col justify-center items-center h-max min-h-screen bg-slate-900 text-center font-mono p-1">
        <h1 className="text-yellow-400 text-7xl mb-2">gyattifier</h1>
        <h2 className="text-slate-400 text-lg">i like big butts and i cannot lie</h2>
        <div className="mx-20 flex-row justify-center items-center bg-slate-200 p-6 rounded-lg shadow-md my-5">
          <div className="flew-col justify-center items-center mb-5">
            <label htmlFor="file-upload" className="cursor-pointer bg-slate-800 text-white px-4 py-2 rounded-lg shadow-lg hover:bg-slate-400 transition-colors ease-in-out">
              Upload Pic
            </label>
            <input id="file-upload" type="file" accept="image/" onChange={handleImageChange} className="hidden"/>
          </div>
          <div className="relative flex justify-center items-center bg-slate-300 p-6 mx-16 rounded-lg shadow-md mb-5">
            {image && (
              <img src={image} alt="Image" className={`max-w-full max-h-lvh object-contain rounded-lg shadow-lg items-center ${loading ? 'opacity-50' : 'opacity-100'} transition-opacity ease-in-out`}/>
            )}
            {loading && (
              <div className="absolute top-0 left-0 w-full h-full flex justify-center items-center z-10"> 
                <ClipLoader size={120} color="#475569"/>
              </div>
            )}
          </div>
          <button onClick={uploadImage} className="rounded-lg bg-yellow-300 p-3 text-slate-700 shadow-md hover:bg-yellow-400 transition-colors ease-in-out">make ass bigger</button>
        </div>
      </div>
  )
} 
