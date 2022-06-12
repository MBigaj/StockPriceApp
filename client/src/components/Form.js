import React, { useState } from 'react'

const Form = (props) => {

  const onSubmit = (event) => {
    event.preventDefault()

    const days = event.target[0].value
    const company = event.target[1].value
    const data = { days, company }

    if (days === '') alert('Please enter all fields!')
    else if (days < 1 || days > 365) alert('Only values between 1 - 365 accepted!')
    else
    {
        fetch('/main', {
            'method': 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(() => {
            console.log('ADDED')
        })
    }
  }

  return (
    <form onSubmit={onSubmit} method='POST' className='form'>
      <div>
          <input type='number' placeholder='1 - 365' name='prediction_period' className='text-field'/> <br></br>
      </div>

      <div>
        <label className='text'>Choose a company:</label>
          <select name="company" className='select-field'>
            <option value="AAPL">Apple</option>
            <option value="TSLA">Tesla</option>
          </select> <br></br>
      </div>

      <div>
        <button type='submit' className='btn'>
          Predict 
        </button>
      </div>
    </form>
  )
}

export default Form