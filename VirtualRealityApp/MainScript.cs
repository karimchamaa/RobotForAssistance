using UnityEngine;
using System.Collections;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.IO;
using UnityEngine.UI;

public class MainScript : MonoBehaviour {
    //Texts
    public Text SetDistance;
    public Text SetAngle;
    //TCP Variables
    public String host = "192.168.43.198";
    public Int32 port = 5005;
    internal Boolean socket_ready = false;
    TcpClient tcp_socket;
    NetworkStream net_stream;
    StreamWriter socket_writer;
    StreamReader socket_reader;
    //Object Position
    public int XGoal = 0;
    public int YGoal = 0;
    public int ColorGoal = 0;
    //Robot Position
    public int AngleRobot = 0;
    public float DistanceTravelled = 0f;
    //My Camera is in the VR?
    public int OverheadVR=0;
    void Start()
    {
        //Hide VRs
        GameObject.Find("RobotQuad").GetComponent<Renderer>().enabled = false;
        GameObject.Find("OverHeadQuad").GetComponent<Renderer>().enabled = false;
        //Screen.orientation = ScreenOrientation.Landscape;
        SetDistance.text = (DistanceTravelled*10).ToString()+" cm";
        SetAngle.text = AngleRobot.ToString()+" deg.";
    }
    void Update () {
        //Return back to scene when phone is flipped
        if (Input.deviceOrientation == DeviceOrientation.Portrait && OverheadVR == 1)
        {
            GameObject.Find("Pointer").GetComponent<Renderer>().enabled = true;
            GameObject.Find("Directional Light").GetComponent<Light>().enabled = true;
            GameObject.Find("OverHeadQuad").transform.localScale = new Vector3(0, 0, 0);
            GameObject.Find("VRMain").transform.position = new Vector3(0, 5, 0);
            GameObject.Find("OverHeadQuad").GetComponent<Renderer>().enabled = false;
            OverheadVR = 0;
        }
        //Keep Application Running in Background
        Application.runInBackground = true;
        // Read Data and Extract Position
        string received_data = readSocket();
        if (received_data != "")
        {
            if (received_data.Length == 1)//Distance Travelled
            {
                if (received_data == "3")
                {
                    DistanceTravelled = 3.3f;

                }
                else
                {
                    DistanceTravelled = 4.69f;
                }
                Debug.Log("DistanceTravelled:" + DistanceTravelled);
                GameObject.Find("iRobot").transform.Translate(Vector3.left * DistanceTravelled, Space.Self);
                SetDistance.text = (DistanceTravelled * 10).ToString() + " cm";
            }
            else
            {
                AngleRobot = Int32.Parse(received_data);
                AngleRobot = AngleRobot - 100;
                Debug.Log("Turn by:" + AngleRobot);
                GameObject.Find("iRobot").transform.Rotate(Vector3.up * AngleRobot, Space.World);
                SetAngle.text = AngleRobot.ToString()+" deg.";
            }
        }
    }
    //Object Position and Color
    public void yellowball()
    {
        Debug.Log("Yellow Pressed");
        //xpython=xunity+12.2; ypython=yunity+10.55, divinding by the scale +1
        XGoal = (int)((transform.position.x + 12.2)*(7/24.4))+1;
        YGoal = (int)((transform.position.z + 10.55)*(6/21.1))+1;
        int r = (int)transform.GetComponent<Renderer>().material.color.r;
        int b = (int)transform.GetComponent<Renderer>().material.color.b;
        int g = (int)transform.GetComponent<Renderer>().material.color.g;
        ColorGoal=ExtractColor(r,b,g);
        GoCatchIt(XGoal, YGoal, ColorGoal);
    }
    public void blueball()
    {
        Debug.Log("Blue Pressed");
        //xpython=xunity+12.2; ypython=yunity+10.55, divinding by the scale + 1
        XGoal = (int)((GameObject.Find("BlueBall").transform.position.x + 12.2)*(7/24.4))+1;
        YGoal = (int)((GameObject.Find("BlueBall").transform.position.z + 10.55)*(6/21.1))+1;
        int r = (int)GameObject.Find("BlueBall").transform.GetComponent<Renderer>().material.color.r;
        int b = (int)GameObject.Find("BlueBall").transform.GetComponent<Renderer>().material.color.b;
        int g = (int)GameObject.Find("BlueBall").transform.GetComponent<Renderer>().material.color.g;
        ColorGoal = ExtractColor(r, b, g);
        GoCatchIt(XGoal, YGoal, ColorGoal);
    }
    public void GoCatchIt(int X, int Y, int C)
    {
        string TCPGoal = "";
        //Join Values in a String Format
        TCPGoal = X.ToString() + Y.ToString() + C.ToString();
        writeSocket(TCPGoal);
    }
    public int ExtractColor(int r, int b, int g)
    {
        int ColorValue = 0;
        if (r==1 && b==0 && g==1)//Yellow
        {
            ColorValue = 2;
        }
        if (r == 0 && b == 1 && g == 0)//Blue
        {
            ColorValue = 1;
        }
        return ColorValue;
    }
    //VR Camera Menu
    public void OverheadCamera()
    {
        GameObject.Find("Pointer").GetComponent<Renderer>().enabled = false;
        GameObject.Find("Directional Light").GetComponent< Light>().enabled = false;
        GameObject.Find("OverHeadQuad").transform.localScale = new Vector3(3, 3, 3);
        GameObject.Find("VRMain").transform.position = new Vector3(9000, 9000, 9000);
        GameObject.Find("OverHeadQuad").GetComponent<Renderer>().enabled = true;
        OverheadVR = 1;
    }
    //Settings Menu
    public void ToggleVRMode()
    {
        GvrViewer.Instance.VRModeEnabled = !GvrViewer.Instance.VRModeEnabled;
    }
    public void ToggleDistortionCorrection()
    {
        GvrViewer.Instance.DistortionCorrectionEnabled =
          !GvrViewer.Instance.DistortionCorrectionEnabled;
    }
#if !UNITY_HAS_GOOGLEVR || UNITY_EDITOR
    public void ToggleDirectRender()
    {
        GvrViewer.Controller.directRender = !GvrViewer.Controller.directRender;
    }
#endif  //  !UNITY_HAS_GOOGLEVR || UNITY_EDITOR
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
