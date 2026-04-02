import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  TouchableWithoutFeedback,
  Keyboard,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  SafeAreaView,
  StatusBar,
  Animated,
  Easing,
} from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { Audio } from 'expo-av';
import Svg, { Circle } from 'react-native-svg';
import { BlurView } from 'expo-blur';

const AnimatedCircle = Animated.createAnimatedComponent(Circle);

// --- Constants ---

const THEMES = {
  light: {
    isLight: true,
    background: '#fafafa',
    surface: '#f0f0f0',
    primary: '#4078f2',
    work: '#4CAF50',
    rest: '#F44336',
    text: '#383a42',
    textSecondary: '#a0a1a7',
  },
  dark: {
    isLight: false,
    background: '#1a1d23',
    surface: '#21252b',
    primary: '#61afef',
    work: '#4CAF50',
    rest: '#F44336',
    text: '#abb2bf',
    textSecondary: '#5c6370',
  },
};

const SOUNDS = {
  work: 'https://assets.mixkit.co/active_storage/sfx/212/212-preview.mp3',
  rest: 'https://assets.mixkit.co/active_storage/sfx/2869/2869-preview.mp3',
};

// --- Helper Components ---

const PickerSection = ({ label, value, onValueChange, items, color }) => (
  <View style={styles.pickerSection}>
    <Text style={[styles.pickerLabel, { color }]}>{label}</Text>
    <Picker selectedValue={value} onValueChange={onValueChange} style={styles.picker} itemStyle={styles.pickerItem}>
      {items}
    </Picker>
  </View>
);

// --- Main Application ---

export default function App() {
  // Appearance State
  const [themeKey, setThemeKey] = useState('dark');
  const COLORS = THEMES[themeKey];

  // Timer Configuration State
  const [workTime, setWorkTime] = useState(45);
  const [restTime, setRestTime] = useState(15);
  const [sets, setSets] = useState(8);

  // Timer Execution State
  const [timeLeft, setTimeLeft] = useState(workTime);
  const [currentSet, setCurrentSet] = useState(1);
  const [isWorking, setIsWorking] = useState(true);
  const [isActive, setIsActive] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  const [flashColor, setFlashColor] = useState(null);

  // Animation State
  const progressAnim = useRef(new Animated.Value(1)).current;

  // Refs for persistent objects
  const timerRef = useRef(null);
  const workSoundRef = useRef(null);
  const restSoundRef = useRef(null);

  // Audio Initialization
  useEffect(() => {
    async function setupAudio() {
      try {
        await Audio.setAudioModeAsync({
          playsInSilentModeIOS: true,
          staysActiveInBackground: true,
          shouldDuckAndroid: true,
        });

        const { sound: workSound } = await Audio.Sound.createAsync({ uri: SOUNDS.work });
        workSoundRef.current = workSound;

        const { sound: restSound } = await Audio.Sound.createAsync({ uri: SOUNDS.rest });
        restSoundRef.current = restSound;
      } catch (error) {
        console.error('Audio setup failed', error);
      }
    }

    setupAudio();

    return () => {
      if (workSoundRef.current) workSoundRef.current.unloadAsync().catch(() => {});
      if (restSoundRef.current) restSoundRef.current.unloadAsync().catch(() => {});
    };
  }, []);

  // Timer Logic
  useEffect(() => {
    if (isActive && timeLeft > 0) {
      timerRef.current = setInterval(() => setTimeLeft((p) => p - 1), 1000);
      
      // Start smooth animation
      Animated.timing(progressAnim, {
        toValue: 0,
        duration: timeLeft * 1000,
        easing: Easing.linear,
        useNativeDriver: false,
      }).start();

    } else if (timeLeft === 0) {
      handleIntervalEnd();
    } else {
      clearInterval(timerRef.current);
      progressAnim.stopAnimation();
    }
    return () => clearInterval(timerRef.current);
  }, [isActive, timeLeft === 0]); // Only re-run when isActive changes or timer hits 0

  const handleIntervalEnd = () => {
    clearInterval(timerRef.current);
    progressAnim.stopAnimation();
    
    if (isWorking) {
      if (currentSet < sets) {
        setIsWorking(false);
        setTimeLeft(restTime);
        progressAnim.setValue(1);
        triggerTransition('rest');
      } else {
        finishWorkout();
      }
    } else {
      setIsWorking(true);
      setCurrentSet((p) => p + 1);
      setTimeLeft(workTime);
      progressAnim.setValue(1);
      triggerTransition('work');
    }
  };

  const triggerTransition = async (type) => {
    const sound = type === 'work' ? workSoundRef.current : restSoundRef.current;
    const colors = { work: COLORS.work, rest: COLORS.rest, finish: COLORS.primary };
    const color = colors[type] || COLORS.primary;
    
    if (sound) {
      try {
        await sound.stopAsync();
        await sound.playAsync();
        // Stop sound after exactly 1 second
        setTimeout(async () => {
          try {
            await sound.stopAsync();
          } catch (e) {
            // Ignore errors if sound already stopped or unloaded
          }
        }, 1000);
      } catch (error) {
        console.error('Playback failed', error);
      }
    }
    
    setFlashColor(color);
    setTimeout(() => setFlashColor(null), 1000);
  };

  const finishWorkout = () => {
    setIsActive(false);
    setIsFinished(true);
    setTimeLeft(0);
    progressAnim.setValue(0);
    triggerTransition('finish');
  };

  const toggleTimer = () => {
    if (isFinished) resetTimer();
    else setIsActive(!isActive);
  };

  const resetTimer = () => {
    clearInterval(timerRef.current);
    progressAnim.stopAnimation();
    setIsActive(false);
    setIsWorking(true);
    setCurrentSet(1);
    setTimeLeft(workTime);
    progressAnim.setValue(1);
    setIsFinished(false);
    setFlashColor(null);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const renderPickerItems = (max, step = 1, isTime = true) => {
    const items = [];
    for (let i = step; i <= max; i += step) {
      const label = isTime ? formatTime(i) : i.toString();
      items.push(<Picker.Item key={i} label={label} value={i} color={COLORS.text} />);
    }
    return items;
  };

  // Progress Ring Calculations
  const size = 360;
  const strokeWidth = 24;
  const center = size / 2;
  const radius = center - strokeWidth;
  const circumference = 2 * Math.PI * radius;
  
  const strokeDashoffset = progressAnim.interpolate({
    inputRange: [0, 1],
    outputRange: [circumference, 0],
  });

  return (
    <SafeAreaView style={[styles.safeArea, { backgroundColor: COLORS.background }]}>
      <StatusBar barStyle={COLORS.isLight ? 'dark-content' : 'light-content'} />
      <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
        <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={styles.container}>
          <ScrollView contentContainerStyle={styles.scrollContent}>
            
            {/* Theme Selector */}
            <View style={styles.themeSwitcher}>
              {['light', 'dark'].map((key) => (
                <TouchableOpacity
                  key={key}
                  style={[styles.themeButton, themeKey === key && { backgroundColor: COLORS.primary }]}
                  onPress={() => setThemeKey(key)}
                >
                  <Text style={[styles.themeButtonText, { 
                    color: themeKey === key ? (COLORS.isLight ? '#fff' : COLORS.background) : COLORS.textSecondary 
                  }]}>
                    {key.toUpperCase()}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>

            {/* Timer Display */}
            <View style={styles.timerContainer}>
              <View style={styles.glassWrapper}>
                <BlurView
                  intensity={Platform.OS === 'ios' ? 80 : 100}
                  tint={COLORS.isLight ? 'extraLight' : 'dark'}
                  style={[styles.timerCircle, { 
                    backgroundColor: flashColor || (COLORS.isLight ? 'rgba(255,255,255,0.2)' : 'rgba(20,20,20,0.3)'),
                  }]}
                >
                  <Svg width={size} height={size} style={styles.progressSvg}>
                    {/* Glass Rim */}
                    <Circle
                      cx={center}
                      cy={center}
                      r={center - 0.5}
                      stroke={COLORS.isLight ? 'rgba(255,255,255,0.8)' : 'rgba(255,255,255,0.15)'}
                      strokeWidth={1}
                      fill="none"
                    />
                    
                    {/* Background Track */}
                    <Circle
                      cx={center}
                      cy={center}
                      r={radius}
                      stroke={COLORS.isLight ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.05)'}
                      strokeWidth={strokeWidth}
                      fill="none"
                    />
                    {/* Animated Progress Ring */}
                    <AnimatedCircle
                      cx={center}
                      cy={center}
                      r={radius}
                      stroke={isFinished ? COLORS.primary : isWorking ? COLORS.work : COLORS.rest}
                      strokeWidth={strokeWidth}
                      fill="none"
                      strokeDasharray={circumference}
                      strokeDashoffset={strokeDashoffset}
                      strokeLinecap="round"
                      rotation="-90"
                      originX={center}
                      originY={center}
                    />
                  </Svg>

                  <Text style={[styles.statusText, { color: flashColor ? COLORS.background : COLORS.textSecondary }]}>
                    {isFinished ? 'DONE!' : isWorking ? 'WORKOUT' : 'REST'}
                  </Text>
                  <Text style={[styles.timerText, { color: flashColor ? (COLORS.isLight ? '#fff' : COLORS.background) : COLORS.text }]} 
                        numberOfLines={1} adjustsFontSizeToFit>
                    {formatTime(timeLeft)}
                  </Text>
                  <Text style={[styles.setCount, { color: flashColor ? COLORS.background : COLORS.textSecondary }]}>
                    SET {currentSet} / {sets}
                  </Text>
                </BlurView>
              </View>
            </View>

            {/* Controls */}
            <View style={styles.controls}>
              <TouchableOpacity style={[styles.button, { backgroundColor: COLORS.primary }]} onPress={toggleTimer}>
                <Text style={[styles.buttonText, { color: (COLORS.isLight && !isActive) ? '#fff' : COLORS.background }]}>
                  {isActive ? 'PAUSE' : isFinished ? 'RESTART' : 'START'}
                </Text>
              </TouchableOpacity>

              <TouchableOpacity style={[styles.resetButton, { borderColor: COLORS.textSecondary }]} onPress={resetTimer}>
                <Text style={[styles.resetButtonText, { color: COLORS.textSecondary }]}>RESET</Text>
              </TouchableOpacity>
            </View>

            {/* Settings */}
            <View style={styles.settingsContainer}>
              <View style={[styles.pickerGrid, (isActive || isFinished) && styles.hiddenSettings]}>
                <View style={styles.pickerRow}>
                  <PickerSection label="WORKOUT" value={workTime} onValueChange={(v) => { setWorkTime(v); if(isWorking) setTimeLeft(v); }} items={renderPickerItems(600, 5)} color={COLORS.textSecondary} />
                  <PickerSection label="REST" value={restTime} onValueChange={(v) => { setRestTime(v); if(!isWorking) setTimeLeft(v); }} items={renderPickerItems(300, 5)} color={COLORS.textSecondary} />
                  <PickerSection label="SETS" value={sets} onValueChange={setSets} items={renderPickerItems(50, 1, false)} color={COLORS.textSecondary} />
                </View>
              </View>
            </View>

          </ScrollView>
        </KeyboardAvoidingView>
      </TouchableWithoutFeedback>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1 },
  container: { flex: 1 },
  scrollContent: {
    flexGrow: 1,
    alignItems: 'center',
    paddingTop: '25%',
    paddingBottom: 40,
  },
  themeSwitcher: {
    flexDirection: 'row',
    marginBottom: 15,
    backgroundColor: 'rgba(128,128,128,0.1)',
    borderRadius: 18,
    padding: 4,
  },
  themeButton: { paddingHorizontal: 20, paddingVertical: 8, borderRadius: 14 },
  themeButtonText: { fontSize: 12, fontWeight: 'bold' },
  timerContainer: { marginBottom: 20 },
  timerCircle: {
    width: 360,
    height: 360,
    borderRadius: 180,
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusText: { fontSize: 24, fontWeight: '600', marginBottom: 5 },
  timerText: { fontSize: 92, fontWeight: 'bold', textAlign: 'center', width: '95%' },
  setCount: { fontSize: 22, marginTop: 5 },
  controls: {
    flexDirection: 'row',
    width: '100%',
    paddingHorizontal: 20,
    marginBottom: 20,
    gap: 15,
  },
  button: { flex: 1, height: 54, borderRadius: 27, alignItems: 'center', justifyContent: 'center' },
  buttonText: { fontSize: 18, fontWeight: 'bold' },
  resetButton: { flex: 1, height: 54, borderRadius: 27, borderWidth: 2, alignItems: 'center', justifyContent: 'center' },
  resetButtonText: { fontSize: 16, fontWeight: '600' },
  settingsContainer: { height: 300, width: '100%', alignItems: 'center', overflow: 'hidden' },
  pickerGrid: { width: '100%', alignItems: 'center' },
  hiddenSettings: { opacity: 0, pointerEvents: 'none' },
  pickerRow: { flexDirection: 'row', width: '100%', paddingHorizontal: 10, height: 140 },
  pickerSection: { flex: 1, alignItems: 'center' },
  pickerLabel: { fontSize: 10, fontWeight: 'bold', letterSpacing: 1, marginBottom: -10 },
  picker: { width: '100%', height: 120 },
  pickerItem: { fontSize: 14, height: 120 },
  glassWrapper: {
    borderRadius: 180,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 15 },
    shadowRadius: 25,
    shadowOpacity: 0.4,
    elevation: 15,
  },
  progressSvg: {
    position: 'absolute',
    top: 0,
    left: 0,
  },
});
