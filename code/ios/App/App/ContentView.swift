import SwiftUI

struct ContentView: View {
    @State var loaded = false

    init() {
        self.loadResources()
    }

    func loadResources() {
        // TODO this is where I'll pre-load the strictly necessary resources for the main screen
        loaded = true
    }
    
    var body: some View {
        let loadingView = VStack {
            Image(systemName: "globe")
                .imageScale(.large)
                .foregroundStyle(.tint)
            Text("ExerciseLog")
        }
        .padding()
        return Group {
            if loaded {
                SessionSelectorView()
            } else {
                loadingView
            }
        }
    }
}



#Preview {
    ContentView()
}
