import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import './component-css.css'
import { faClose } from '@fortawesome/free-solid-svg-icons'
import React, { useEffect, useState } from 'react'

const Welcome= () =>{
    const [showWelcome, setShowWelcome] = useState();
    useEffect(() => {
      const data = JSON.parse(localStorage.getItem("show_app_intro")) ?? true
      setShowWelcome(data)

    }, [])

    const onHideWelcome = () =>{
        setShowWelcome(false)
        localStorage.setItem('show_app_intro', JSON.stringify(false))
    }
    return (
        <React.Fragment>
        { showWelcome &&
        (<div className='container' >
            <div class="welcome-popup">
                <FontAwesomeIcon
                icon={faClose}
                style={{float: 'right', margin: '5px'}}
                onClick={onHideWelcome} />
                <p>به فروشگاه ما خوش آمدید! از تجربه خرید خود لذت ببرید.</p>
                <button class="close-btn" onClick={onHideWelcome} >بستن</button>
            </div>
        </div>
        )}
        </React.Fragment>
    )
}

export default Welcome
