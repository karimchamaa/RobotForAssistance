using UnityEngine;
using System.Collections;
using System.IO;

public class LoadRobotImages : MonoBehaviour {    
    IEnumerator Start() {
        while (true){ 
        WWW www = new WWW("http://192.168.43.124/cam_pic.php?time");
        yield return www;
        Texture2D texture = www.texture;
        this.GetComponent<Renderer>().material.mainTexture = texture;
    }
    }
}

