using UnityEngine;
using System.Collections;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.IO;
using UnityEngine.UI;

public class Servo : MonoBehaviour {
    //TCP Variables
    public String host = "192.168.43.124";
    public Int32 port = 5005;
    internal Boolean socket_ready = false;
    TcpClient tcp_socket;
    NetworkStream net_stream;
    StreamWriter socket_writer;
    StreamReader socket_reader;
    //Servo Stereopic Position
    public int ServoRange = 5; 
    public int ServoX = 0;
    public int ServoY = 0;
    public string ServoTCP = "";
    //Servo old positions
    public int ServoXStored;
    public int ServoYStored;

    //My Camera is in the VR?
    public int RobotVR = 0;

    void Start () {
        //Screen.orientation = ScreenOrientation.Landscape;
        ServoXStored = 2*ServoRange;
        ServoYStored = 2*ServoRange;
	}

	void Update () {
        //Keep Application Running in Background
        Application.runInBackground = true;
        //Return back to scene when phone is flipped
        if (Input.deviceOrientation == DeviceOrientation.Portrait && RobotVR == 1)
        {
            GameObject.Find("Pointer").GetComponent<Renderer>().enabled = true;
            GameObject.Find("Directional Light").GetComponent<Light>().enabled = true;
            GameObject.Find("RobotQuad").transform.localScale = new Vector3(0, 0, 0);
            GameObject.Find("VRMain").transform.position = new Vector3(0, 5, 0);
            GameObject.Find("RobotQuad").GetComponent<Renderer>().enabled = false;
            RobotVR = 0;
        }
        //Get Head Position - Controling 2-DOF Servos
        ServoX = (int)(((float)Camera.main.transform.rotation[1] * 90.0) + 90.0); ; //Horizontal
        ServoY = (int)(((float)Camera.main.transform.rotation[0] * -90.0) + 90.0);//Vertical Upward -1 
        if (( Math.Abs(ServoX-ServoXStored)>=ServoRange || Math.Abs(ServoY - ServoYStored) >= ServoRange) && RobotVR==1)
        {
            ServoTCP = (ServoX + 100).ToString() + (ServoY + 100).ToString();//Combine Servo in String
            writeSocket(ServoTCP);
            ServoXStored = ServoX;
            ServoYStored = ServoY;
        }
    }
    //VR Camera Menu
    public void RobotCamera()
    {
        GameObject.Find("Pointer").GetComponent<Renderer>().enabled = false;
        GameObject.Find("Directional Light").GetComponent<Light>().enabled = false;
        GameObject.Find("RobotQuad").transform.localScale = new Vector3(3, 3, 3);
        GameObject.Find("VRMain").transform.position = new Vector3(9000, 9000, 9000);
        GameObject.Find("RobotQuad").GetComponent<Renderer>().enabled = true;
        RobotVR = 1;
    }
    //TCP Functions
    void Awake()
    {
        setupSocket();
    }
    void OnApplicationQuit()
    {
        closeSocket();
    }
    public void setupSocket()
    {
        try
        {
            tcp_socket = new TcpClient(host, port);
            net_stream = tcp_socket.GetStream();
            socket_writer = new StreamWriter(net_stream);
            socket_reader = new StreamReader(net_stream);
            socket_ready = true;
        }
        catch (Exception e)
        {
            // Something went wrong
            Debug.Log("Socket error: " + e);
        }
    }
    public void writeSocket(string line)
    {
        if (!socket_ready)
            return;
        line = line + "\r\n";
        socket_writer.Write(line);
        socket_writer.Flush();
    }
    public String readSocket()
    {
        if (!socket_ready)
            return "";
        if (net_stream.DataAvailable)
            return socket_reader.ReadLine();
        return "";
    }
    public void closeSocket()
    {
        if (!socket_ready)
            return;
        socket_writer.Close();
        socket_reader.Close();
        tcp_socket.Close();
        socket_ready = false;
    }
}
