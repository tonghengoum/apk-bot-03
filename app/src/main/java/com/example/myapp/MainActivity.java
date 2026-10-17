package com.example.myapp;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private TextView textView;
    private boolean isTextToggled = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        textView = findViewById(R.id.textView);
        Button toggleTextButton = findViewById(R.id.buttonToggleText);
        Button startServiceButton = findViewById(R.id.buttonStartService);
        Button stopServiceButton = findViewById(R.id.buttonStopService);

        toggleTextButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                isTextToggled = !isTextToggled;
                textView.setText(isTextToggled ? &quot;Button clicked!&quot; : &quot;Hello, World!&quot;);
            }
        });

        startServiceButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent serviceIntent = new Intent(MainActivity.this, RemoteControlService.class);
                serviceIntent.setAction(&quot;com.example.myapp.action.START&quot;);
                startService(serviceIntent);
            }
        });

        stopServiceButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent serviceIntent = new Intent(MainActivity.this, RemoteControlService.class);
                serviceIntent.setAction(&quot;com.example.myapp.action.STOP&quot;);
                startService(serviceIntent);
            }
        });
    }
}