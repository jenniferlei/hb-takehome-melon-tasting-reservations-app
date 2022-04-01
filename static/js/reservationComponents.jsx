"use strict";

// possible appointment start and end times
const appointmentTimes = [
  ["00:00", "00:30", 1],
  ["00:30", "01:00", 2],
  ["01:00", "01:30", 3],
  ["01:30", "02:00", 4],
  ["02:00", "02:30", 5],
  ["02:30", "03:00", 6],
  ["03:00", "03:30", 7],
  ["03:30", "04:00", 8],
  ["04:00", "04:30", 9],
  ["04:30", "05:00", 10],
  ["05:00", "05:30", 11],
  ["05:30", "06:00", 12],
  ["06:00", "06:30", 13],
  ["06:30", "07:00", 14],
  ["07:00", "07:30", 15],
  ["07:30", "08:00", 16],
  ["08:00", "08:30", 17],
  ["08:30", "09:00", 18],
  ["09:00", "09:30", 19],
  ["09:30", "10:00", 20],
  ["10:00", "10:30", 21],
  ["10:30", "11:00", 22],
  ["11:00", "11:30", 23],
  ["11:30", "12:00", 24],
  ["12:00", "12:30", 25],
  ["12:30", "13:00", 26],
  ["13:00", "13:30", 27],
  ["13:30", "14:00", 28],
  ["14:00", "14:30", 29],
  ["14:30", "15:00", 30],
  ["15:00", "15:30", 31],
  ["15:30", "16:00", 32],
  ["16:00", "16:30", 33],
  ["16:30", "17:00", 34],
  ["17:00", "17:30", 35],
  ["17:30", "18:00", 36],
  ["18:00", "18:30", 37],
  ["18:30", "19:00", 38],
  ["19:00", "19:30", 39],
  ["19:30", "20:00", 40],
  ["20:00", "20:30", 41],
  ["20:30", "21:00", 42],
  ["21:00", "21:30", 43],
  ["21:30", "22:00", 44],
  ["22:00", "22:30", 45],
  ["22:30", "23:00", 46],
  ["23:00", "23:30", 47],
  ["23:30", "24:00", 48],
];

const ViewReservation = (props) => {
  // Table rows for viewing user's existing reservations and modals to delete existing reservations

  // unpack props
  const { reservationId, date, startTime, endTime } = props;

  // Convert 24 hour time to 12 hour time format
  const convertTimeFormat = (time) => {
    const timeHours = time.slice(0, 2);
    const timeHoursConverted = String(((Number(timeHours) + 11) % 12) + 1);
    const timeMins = time.slice(3, 5);
    const timeSuffix = timeHours < 12 ? "AM" : "PM";
    const updatedTimeString =
      timeHoursConverted + ":" + timeMins + " " + timeSuffix;
    return updatedTimeString;
  };

  // Convert date to yyyy-mm-dd to mm/dd/yy format
  const dateFormatted =
    date.slice(5, 7) + "/" + date.slice(8, 10) + "/" + date.slice(2, 4);

  // Confirm user would like to delete reservation. Delete reservation once validated
  const deleteReservation = () => {
    const validate = confirm("Do you want to delete this reservation?");
    if (validate) {
      fetch(`/delete-reservation/${reservationId}`, {
        method: "DELETE",
      }).then((response) => {
        response.json().then((jsonResponse) => {
          props.getReservations(); // lift state up to ViewReservationContainer (show reservations without deleted reservation)
        });
      });
    }
  };

  return (
    <tr id={reservationId}>
      <td>{dateFormatted}</td>
      <td>{convertTimeFormat(startTime)}</td>
      <td>{convertTimeFormat(endTime)}</td>
      <td>
        <button
          type="button"
          className="btn btn-outline-dark"
          style={{ borderRadius: "50%", padding: "0 7.5px" }}
          onClick={deleteReservation}
        >
          -
        </button>
      </td>
    </tr>
  );
};

const ViewReservationContainer = React.forwardRef((props, ref) => {
  // Container of all table rows for viewing user's existing reservations

  const [reservations, setReservations] = React.useState([]);

  React.useEffect(() => {
    getReservations();
  }, []);

  // get logged in user's existing reservations
  const getReservations = () => {
    fetch("/reservations.json")
      .then((response) => response.json())
      .then((responseJson) => {
        const { reservations } = responseJson;
        setReservations(reservations);
      });
  };

  // Access getReservations function from parent ReservationContainer
  React.useImperativeHandle(ref, () => ({
    getReservations() {
      fetch("/reservations.json")
        .then((response) => response.json())
        .then((responseJson) => {
          const { reservations } = responseJson;
          setReservations(reservations);
        });
    },
  }));

  const timestamp = Date.now();

  // Create ViewReservation components for each of user's reservations
  const allReservations = reservations.map((reservation) => (
    <ViewReservation
      key={`${timestamp}-${reservation.reservation_id}`}
      reservationId={reservation.reservation_id}
      date={reservation.date}
      startTime={reservation.start_time}
      endTime={reservation.end_time}
      getReservations={getReservations}
    />
  ));

  return (
    <div className="table-overflow">
      <h3>Your Reservations</h3>
      <table className="table table-striped table-sm">
        <thead>
          <tr>
            <th role="columnheader">Date</th>
            <th role="columnheader">Start Time</th>
            <th role="columnheader">End Time</th>
            <th role="columnheader">Delete</th>
          </tr>
        </thead>
        <tbody>{allReservations}</tbody>
      </table>
    </div>
  );
});

const OpenReservation = (props) => {
  // Table rows for reservations search results and modals to add new reservations

  // unpack props
  const { reserveId, date, startTime, endTime } = props;

  // Convert 24 hour time to 12 hour time format
  const convertTimeFormat = (time) => {
    const timeHours = time.slice(0, 2);
    const timeHoursConverted = String(((Number(timeHours) + 11) % 12) + 1);
    const timeMins = time.slice(3, 5);
    const timeSuffix = timeHours < 12 ? "AM" : "PM";
    const updatedTimeString =
      timeHoursConverted + ":" + timeMins + " " + timeSuffix;
    return updatedTimeString;
  };

  const startTimeFormatted = convertTimeFormat(startTime);
  const endTimeFormatted = convertTimeFormat(endTime);

  // Convert date to yyyy-mm-dd to mm/dd/yy format
  const dateFormatted =
    date.slice(5, 7) + "/" + date.slice(8, 10) + "/" + date.slice(2, 4);

  // Check if user already has a reservation for the date. If not, create reservation
  const addReservation = () => {
    fetch("/reservations.json")
      .then((response) => response.json())
      .then((responseJson) => {
        const { reservations } = responseJson;
        if (reservations.some((reservation) => reservation.date === date)) {
          alert(
            "You already have a reservation for this date. Please search for a different date."
          );
        } else {
          fetch("/add-reservation", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Accept: "application/json",
            },
            body: JSON.stringify({
              date,
              startTime,
              endTime,
            }),
          }).then((response) => {
            response.json().then((jsonResponse) => {
              props.parentGetReservations(); // lift state up to SearchReservation
            });
          });
        }
      });
  };

  return (
    <React.Fragment>
      <tr>
        <td>{dateFormatted}</td>
        <td>{startTimeFormatted}</td>
        <td>{endTimeFormatted}</td>
        <td>
          <button
            type="button"
            className="btn btn-outline-dark"
            style={{ borderRadius: "50%", padding: "0 7.5px" }}
            data-bs-toggle="modal"
            data-bs-target={`#add-reservation-${reserveId}`}
          >
            +
          </button>
        </td>
      </tr>

      <div
        className="modal fade"
        id={`add-reservation-${reserveId}`}
        tabIndex="-1"
        aria-labelledby={`add-reservation-${reserveId}-label`}
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5
                className="modal-title"
                id={`add-reservation-${reserveId}-label`}
              >
                Add Reservation
              </h5>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body fw-300">
              <div className="mb-3" style={{ textAlign: "center" }}>
                Would you like to create a reservation for
                <br /> {dateFormatted} from {startTimeFormatted} to{" "}
                {endTimeFormatted}?
              </div>
              <div className="modal-footer">
                <button
                  className="btn btn-sm btn-outline-dark btn-block fw-300"
                  type="submit"
                  data-bs-dismiss="modal"
                  onClick={addReservation}
                >
                  Confirm
                </button>
                <button
                  type="button"
                  className="btn btn-sm btn-secondary btn-block fw-300"
                  data-bs-dismiss="modal"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </React.Fragment>
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
    // get username of logged in user
    fetch("/login_session.json")
      .then((response) => response.json())
      .then((responseJson) => {
        setUsername(responseJson.username);
        console.log("TEST", responseJson.username);
      });
  }, []);

  // Check if an existing reservation exists for each time slot. If not, add time slot to available reservations
  const compareWithExistingReservations = (apptTimes, reservations) => {
    let availReservations = [];
    apptTimes.map((timeSlot) => {
      if (
        !reservations.some(
          (reservation) => reservation.start_time === timeSlot[0].concat(":00")
        )
      ) {
        availReservations.push({
          startTime: timeSlot[0],
          endTime: timeSlot[1],
          order: timeSlot[2],
        });
      }
    });
    if (availReservations.length === 0) {
      setErrorMessage(
        "There are no available reservations for this time frame. Please try again."
      );
    } else {
      setErrorMessage(null);
    }
    setOpenReservations(availReservations);
  };

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
            if (reservationStart && reservationEnd) {
              const filteredAppointmentTimes = appointmentTimes.filter(
                (timeSlot) =>
                  timeSlot[0].concat(":00") >= reservationStart &&
                  timeSlot[1].concat(":00") <=
                    reservationEnd.slice(0, 5).concat(":01")
              );
              compareWithExistingReservations(
                filteredAppointmentTimes,
                reservations
              );
            } else if (reservationStart) {
              const filteredAppointmentTimes = appointmentTimes.filter(
                (timeSlot) => timeSlot[0].concat(":00") >= reservationStart
              );
              compareWithExistingReservations(
                filteredAppointmentTimes,
                reservations
              );
            } else if (reservationEnd) {
              const filteredAppointmentTimes = appointmentTimes.filter(
                (timeSlot) => timeSlot[1].concat(":00") <= reservationEnd
              );
              compareWithExistingReservations(
                filteredAppointmentTimes,
                reservations
              );
            } else {
              compareWithExistingReservations(appointmentTimes, reservations);
            }
          }
        });
    }
  };

  // Clear search parameters and results
  const clearSearch = () => {
    setReservationDate("");
    setReservationStart("");
    setReservationEnd("");
    setOpenReservations([]);
  };

  const parentGetReservations = () => {
    props.topParentGetReservations(); // lift state up to ReservationContainer
  };

  const timestamp = Date.now();

  // For each open reservation, create OpenReservation component
  const allOpenReservations = openReservations
    .sort((a, b) => {
      return a.order - b.order;
    })
    .map((reservation) => (
      <OpenReservation
        key={`${timestamp}-${reservation.order}`}
        reserveId={`${timestamp}-${reservation.order}`}
        date={reservationDate}
        startTime={reservation.startTime}
        endTime={reservation.endTime}
        parentGetReservations={parentGetReservations}
      />
    ));

  return (
    <React.Fragment>
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
        <div className="d-flex">
          <button
            type="submit"
            className="btn btn-outline-dark me-2"
            onClick={getOpenReservations}
          >
            Search
          </button>
          <button
            type="submit"
            className="btn btn-outline-dark"
            onClick={clearSearch}
          >
            Clear Search
          </button>
        </div>
      </div>
      <div
        style={{
          height: "calc(80vh - 310px)",
        }}
      >
        <div
          className="table-overflow"
          style={{
            paddingTop: "5px",
          }}
        >
          {errorMessage ? (
            <div>{errorMessage}</div>
          ) : openReservations.length > 0 ? (
            <div>
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
            </div>
          ) : null}
        </div>
      </div>
    </React.Fragment>
  );
};

const ReservationContainer = (props) => {
  // Container for SearchReservation and ViewReservationContainer

  // React hook useRef to access child ViewReservationContainer's getReservation function
  const ViewReservationContainerRef = React.useRef();
  const topParentGetReservations = () => {
    ViewReservationContainerRef.current.getReservations();
  };

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
      <div className="card-body">
        <div className="d-flex" style={{ height: "100%", width: "100%" }}>
          <div className="col-md-6" style={{ height: "100%" }}>
            <SearchReservation
              topParentGetReservations={topParentGetReservations}
            />
          </div>
          <div className="col-md-5 offset-md-1">
            <div style={{ height: "calc(100vh - 180px" }}>
              <ViewReservationContainer ref={ViewReservationContainerRef} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<ReservationContainer />, document.getElementById("root"));
