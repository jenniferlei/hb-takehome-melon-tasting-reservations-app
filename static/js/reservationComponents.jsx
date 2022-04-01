"use strict";

const appointmentTimes = [
  ["00:00", "00:30"],
  ["00:30", "01:00"],
  ["01:00", "01:30"],
  ["01:30", "02:00"],
  ["02:00", "02:30"],
  ["02:30", "03:00"],
  ["03:00", "03:30"],
  ["03:30", "04:00"],
  ["04:00", "04:30"],
  ["04:30", "05:00"],
  ["05:00", "05:30"],
  ["05:30", "06:00"],
  ["06:00", "06:30"],
  ["06:30", "07:00"],
  ["07:00", "07:30"],
  ["07:30", "08:00"],
  ["08:00", "08:30"],
  ["08:30", "09:00"],
  ["09:00", "09:30"],
  ["09:30", "10:00"],
  ["10:00", "10:30"],
  ["10:30", "11:00"],
  ["11:00", "11:30"],
  ["11:30", "12:00"],
  ["12:00", "12:30"],
  ["12:30", "13:00"],
  ["13:00", "13:30"],
  ["13:30", "14:00"],
  ["14:00", "14:30"],
  ["14:30", "15:00"],
  ["15:00", "15:30"],
  ["15:30", "16:00"],
  ["16:00", "16:30"],
  ["16:30", "17:00"],
  ["17:00", "17:30"],
  ["17:30", "18:00"],
  ["18:00", "18:30"],
  ["18:30", "19:00"],
  ["19:00", "19:30"],
  ["19:30", "20:00"],
  ["20:00", "20:30"],
  ["20:30", "21:00"],
  ["21:00", "21:30"],
  ["21:30", "22:00"],
  ["22:00", "22:30"],
  ["22:30", "23:00"],
  ["23:00", "23:30"],
  ["23:30", "00:00"],
];

const ViewReservation = (props) => {
  const convertTimeFormat = (time) => {
    const timeHours = time.slice(0, 2);
    const timeHoursConverted = String(((Number(timeHours) + 11) % 12) + 1);
    const timeMins = time.slice(3, 5);
    const timeSuffix = timeHours <= 12 ? "PM" : "AM";
    const updatedTimeString =
      timeHoursConverted + ":" + timeMins + " " + timeSuffix;
    return updatedTimeString;
  };

  return (
    <tr id={props.reservationId}>
      <td>{props.date}</td>
      <td>{convertTimeFormat(props.startTime)}</td>
      <td>{convertTimeFormat(props.endTime)}</td>
    </tr>
  );
};

const ViewReservationContainer = (props) => {
  const [reservations, setReservations] = React.useState([]);

  React.useEffect(() => {
    fetch("/reservations")
      .then((response) => response.json())
      .then((responseJson) => {
        const { reservations } = responseJson;
        setReservations(reservations);
      });
  }, []);

  const timestamp = Date.now();

  const allReservations = reservations.map((reservation) => (
    <ViewReservation
      key={`${timestamp}-${reservation.reservation_id}`}
      reservationId={reservation.reservation_id}
      date={reservation.date}
      startTime={reservation.start_time}
      endTime={reservation.end_time}
    />
  ));

  return (
    <div>
      <h3>Your Reservations</h3>
      <table className="table table-striped table-sm">
        <thead>
          <tr>
            <th role="columnheader">Date</th>
            <th role="columnheader">Start Time</th>
            <th role="columnheader">End Time</th>
          </tr>
        </thead>
        <tbody>{allReservations}</tbody>
      </table>
    </div>
  );
};

const OpenReservation = (props) => {
  const convertTimeFormat = (time) => {
    const timeHours = time.slice(0, 2);
    const timeHoursConverted = String(((Number(timeHours) + 11) % 12) + 1);
    const timeMins = time.slice(3, 5);
    const timeSuffix = timeHours <= 12 ? "PM" : "AM";
    const updatedTimeString =
      timeHoursConverted + ":" + timeMins + " " + timeSuffix;
    return updatedTimeString;
  };
  return (
    <tr>
      <td>{props.date}</td>
      <td>{convertTimeFormat(props.startTime)}</td>
      <td>{convertTimeFormat(props.endTime)}</td>
      <td>Add</td>
    </tr>
  );
};

const SearchReservation = (props) => {
  const [username, setUsername] = React.useState("");
  const [reservationDate, setReservationDate] = React.useState("");
  const [reservationStart, setReservationStart] = React.useState("");
  const [reservationEnd, setReservationEnd] = React.useState("");

  const [openReservations, setOpenReservations] = React.useState([]);
  const [errorMessage, setErrorMessage] = React.useState(null);

  React.useEffect(() => {
    // fetch all
    fetch("/login_session.json")
      .then((response) => response.json())
      .then((responseJson) => {
        setUsername(responseJson.username);
        console.log("TEST", responseJson.username);
      });
  }, []);

  // fetch reservations based on the date, start time and end time parameters
  // if user already has a reservation on date, show error
  // if none available, show error
  const getOpenReservations = () => {
    if (reservationDate === "") {
      alert("Please input a date");
    } else {
      const queries = ["/search_reservations?"];
      queries.push(`date=${reservationDate}`);
      if (reservationStart !== "") {
        queries.push(`start_time=${reservationStart}`);
      }
      if (reservationEnd !== "") {
        queries.push(`end_time=${reservationEnd}`);
      }
      const queriesUrl = queries.reduce(
        (text, value, i) => text + (i > 1 ? "&" : "") + value
      );

      fetch(queriesUrl)
        .then((response) => response.json())
        .then((responseJson) => {
          const { reservations } = responseJson;
          // If any of the reservations belong to the current user's, set error message
          if (
            reservations.some(
              (reservation) => reservation.username === username
            )
          ) {
            setErrorMessage(
              "You already have a reservation for this date. Please search for a different date."
            );
            console.log("TEST", reservations);
            return;
          } else {
            // If start time is not already reserved, add to available reservation times
            let availReservations = [];
            appointmentTimes.map((timeSlot) => {
              if (
                !reservations.some(
                  (reservation) =>
                    reservation.start_time === timeSlot[0].concat(":00")
                )
              ) {
                availReservations.push({
                  startTime: timeSlot[0],
                  endTime: timeSlot[1],
                });
              }
            });
            if (availReservations.length === 0) {
              setErrorMessage(
                "There are no available reservations for this timeframe. Please try again."
              );
            } else {
              setErrorMessage(null);
            }
            setOpenReservations(availReservations);
          }
        });
    }
  };

  const timestamp = Date.now();

  const allOpenReservations = openReservations.map((reservation) => (
    <OpenReservation
      key={`${timestamp}-${reservationDate}-${reservation.startTime}`}
      date={reservationDate}
      startTime={reservation.startTime}
      endTime={reservation.endTime}
    />
  ));

  return (
    <div>
      <h3>Make A Reservation</h3>
      Enter the Date of the reservation you would like
      <div className="mb-1">
        <label htmlFor="reservationDate"> Date </label>
        <input
          type="date"
          value={reservationDate}
          onChange={(event) => setReservationDate(event.target.value)}
          className="form-control"
          id="reservationDate"
        />
      </div>
      Enter an optional time range and we will only show appointments in that
      range
      <div className="row">
        <div className="col mb-1">
          <label htmlFor="reservationStart"> Start Time </label>
          <input
            type="time"
            value={reservationStart}
            onChange={(event) => setReservationStart(event.target.value)}
            className="form-control"
            id="reservationStart"
          />
        </div>
        <div className="col mb-1">
          <label htmlFor="reservationEnd"> End Time </label>
          <input
            type="time"
            value={reservationEnd}
            onChange={(event) => setReservationEnd(event.target.value)}
            className="form-control"
            id="reservationEnd"
          />
        </div>
      </div>
      <button
        type="submit"
        className="btn btn-outline-dark"
        onClick={getOpenReservations}
      >
        Search
      </button>
      <div style={{ height: "100%", overflowY: "auto" }}>
        {errorMessage ? (
          <div>{errorMessage}</div>
        ) : openReservations.length > 0 ? (
          <React.Fragment>
            <table className="table table-striped table-sm">
              <thead>
                <tr>
                  <th role="columnheader">Date</th>
                  <th role="columnheader">Start Time</th>
                  <th role="columnheader">End Time</th>
                  <th role="columnheader">Add</th>
                </tr>
              </thead>
              <tbody>{allOpenReservations}</tbody>
            </table>
          </React.Fragment>
        ) : null}
      </div>
    </div>
  );
};

const ReservationContainer = (props) => {
  return (
    <div
      className="card"
      style={{
        top: "1.5em",
        width: "90vw",
        height: "80vh",
        margin: "auto",
        backgroundColor: "rgba(255, 255, 255, 0.9)",
      }}
    >
      <div className="card-body d-flex">
        <div className="col-md-6">
          <SearchReservation />
        </div>
        <div className="col-md-5 offset-md-1">
          <ViewReservationContainer />
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<ReservationContainer />, document.getElementById("root"));
